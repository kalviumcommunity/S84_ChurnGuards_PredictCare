import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.validators import (
    validate_customers_schema,
    validate_tickets_schema,
    validate_interactions_schema
)

def calculate_real_risk_score(customer_row, tickets_df, interactions_df):
    """
    Calculate real risk score based on multiple business factors
    
    Risk Components:
    1. Open Tickets (0-25 points)
    2. Last Login Activity (0-20 points)
    3. Sentiment Analysis (0-25 points)
    4. Days Until Renewal (0-20 points)
    5. CSAT Score (0-10 points)
    
    Returns: Risk score from 0-100 (higher = more at risk)
    """
    risk_score = 0
    customer_id = customer_row['customer_id']
    
    # 1. OPEN TICKETS RISK (0-25 points)
    if not tickets_df.empty:
        customer_tickets = tickets_df[tickets_df['customer_id'] == customer_id]
        open_tickets = customer_tickets[customer_tickets['status'].isin(['Open', 'In Progress'])]
        critical_tickets = open_tickets[open_tickets['priority'] == 'Critical']
        
        # Count critical tickets (15 points per critical ticket, max 15)
        risk_score += min(len(critical_tickets) * 5, 15)
        
        # Count all open tickets (2 points per ticket, max 10)
        risk_score += min(len(open_tickets) * 2, 10)
    
    # 2. LAST LOGIN ACTIVITY RISK (0-20 points)
    if pd.notna(customer_row.get('last_activity')):
        try:
            last_activity = pd.to_datetime(customer_row['last_activity'])
            days_since_login = (datetime.now() - last_activity).days
            
            if days_since_login > 30:
                risk_score += 20  # No activity in 30+ days = max risk
            elif days_since_login > 14:
                risk_score += 15  # No activity in 2+ weeks
            elif days_since_login > 7:
                risk_score += 10  # No activity in 1+ week
            elif days_since_login > 3:
                risk_score += 5   # Limited activity
        except:
            risk_score += 10  # Invalid date = moderate risk
    else:
        risk_score += 10  # No activity data = moderate risk
    
    # 3. SENTIMENT ANALYSIS RISK (0-25 points)
    sentiment = customer_row.get('sentiment', 'Neutral')
    if sentiment == 'Negative':
        risk_score += 25
    elif sentiment == 'Neutral':
        risk_score += 10
    # Positive = 0 points
    
    # Check recent interaction sentiment if available
    if not interactions_df.empty:
        recent_interactions = interactions_df[
            (interactions_df['customer_id'] == customer_id) &
            (interactions_df['interaction_type'].isin(['Support Email', 'Phone Call']))
        ].tail(5)
        
        if not recent_interactions.empty:
            negative_count = len(recent_interactions[recent_interactions.get('sentiment') == 'Negative'])
            if negative_count >= 3:
                risk_score += 5  # Multiple negative interactions
    
    # 4. DAYS UNTIL RENEWAL RISK (0-20 points)
    if pd.notna(customer_row.get('renewal_date')):
        try:
            renewal_date = pd.to_datetime(customer_row['renewal_date'])
            days_until_renewal = (renewal_date - datetime.now()).days
            
            if days_until_renewal < 0:
                risk_score += 20  # Past renewal date = critical
            elif days_until_renewal <= 30:
                risk_score += 15  # Renewal within 30 days
            elif days_until_renewal <= 60:
                risk_score += 10  # Renewal within 60 days
            elif days_until_renewal <= 90:
                risk_score += 5   # Renewal within 90 days
        except:
            risk_score += 5  # Invalid date = slight risk
    else:
        risk_score += 5  # No renewal data = slight risk
    
    # 5. CSAT SCORE RISK (0-10 points)
    csat_score = customer_row.get('csat_score', 5)
    try:
        csat = float(csat_score)
        if csat <= 2.0:
            risk_score += 10  # Very low satisfaction
        elif csat <= 3.0:
            risk_score += 7   # Low satisfaction
        elif csat <= 4.0:
            risk_score += 3   # Below average
        # Above 4.0 = 0 points
    except:
        risk_score += 5  # Invalid CSAT = moderate risk
    
    # Cap risk score at 100
    risk_score = min(risk_score, 100)
    
    return int(risk_score)


def calculate_health_status(risk_score):
    """Convert risk score to health status category"""
    if risk_score >= 70:
        return 'Critical'
    elif risk_score >= 50:
        return 'Medium'
    else:
        return 'Low Risk'


@st.cache_data
def load_data():
    """
    Load data from SQLite database instead of CSV files
    This connects the database to the frontend!
    """
    from db_queries import ChurnGuardDB
    
    db = ChurnGuardDB('churnguard.db')
    
    # Load customers from database
    customers = db.execute_query("SELECT * FROM customers")
    
    # Load tickets from database (no JOIN for now, IDs don't match)
    tickets = db.execute_query("SELECT * FROM tickets")
    
    # Load interactions from database  
    interactions = db.execute_query("SELECT * FROM interactions")
    
    # Rename columns to match expected format
    if not interactions.empty and 'interaction_date' in interactions.columns:
        interactions['timestamp'] = interactions['interaction_date']
    
    # Create empty churn_history (not in database yet)
    churn_history = pd.DataFrame()
    
    # Add computed columns for compatibility with existing UI
    if not customers.empty:
        customers['arr'] = customers['arr'].astype(float)
        customers['last_activity'] = pd.to_datetime(customers['last_activity'], errors='coerce')
        customers['company_name'] = customers['company_name'].astype(str)
        
    if not tickets.empty:
        tickets['customer'] = 'User ' + tickets['customer_id'].astype(str)
        tickets['company'] = 'Company ' + tickets['customer_id'].astype(str)
        tickets['risk_score'] = tickets.get('risk_score', 50)
    
    # Apply real risk calculation to all customers
    if not customers.empty:
        customers['risk_score'] = customers.apply(
            lambda row: calculate_real_risk_score(row, tickets, interactions), 
            axis=1
        )
        customers['health_status'] = customers['risk_score'].apply(calculate_health_status)

    return customers, tickets, interactions, churn_history


def filter_customers_by_risk(df, risk_filter):
    """Filter customers based on selected risk levels"""
    if "All Levels" in risk_filter:
        return df
    return df[df['health_status'].isin(risk_filter)]


def calculate_churn_probability(risk_score):
    """Convert risk score to churn probability percentage"""
    if risk_score >= 80:
        return "Very High (>70%)"
    elif risk_score >= 60:
        return "High (50-70%)"
    elif risk_score >= 40:
        return "Medium (30-50%)"
    else:
        return "Low (<30%)"


def get_risk_alert_summary(customers_df):
    """Generate real-time risk alert summary with priority classification"""
    alerts = []
    
    for idx, customer in customers_df.iterrows():
        # High risk score alert
        if customer['risk_score'] >= 80:
            alerts.append({
                'severity': 'Critical',
                'company': customer['company_name'],
                'alert': f"Risk score jumped to {customer['risk_score']}",
                'detail': 'Immediate intervention required',
                'arr': customer['arr'],
                'icon': '🚨'
            })
        
        # Negative sentiment alert
        if customer['sentiment'] == 'Negative' and customer['health_status'] == 'Critical':
            alerts.append({
                'severity': 'High',
                'company': customer['company_name'],
                'alert': 'Negative sentiment with critical health status',
                'detail': 'Customer satisfaction at risk',
                'arr': customer['arr'],
                'icon': '😟'
            })
        
        # Low activity alert
        if pd.notna(customer['last_activity']):
            days_since_activity = (datetime.now() - customer['last_activity']).days
            if days_since_activity > 14 and customer['risk_score'] > 60:
                alerts.append({
                    'severity': 'Medium',
                    'company': customer['company_name'],
                    'alert': f"No activity for {days_since_activity} days",
                    'detail': 'Engagement drop detected',
                    'arr': customer['arr'],
                    'icon': '📉'
                })
    
    # Sort by severity and ARR
    severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
    alerts_sorted = sorted(alerts, key=lambda x: (severity_order.get(x['severity'], 4), -x['arr']))
    
    return alerts_sorted[:10]


def export_customer_data(customers_df):
    """Export customer data with risk metrics and health status"""
    export_data = customers_df[['customer_id', 'company_name', 'risk_score', 'arr', 'health_status', 'sentiment']].copy()
    export_data['last_activity'] = customers_df['last_activity'].dt.strftime('%Y-%m-%d')
    csv = export_data.to_csv(index=False)
    return csv


# SQL QUERY FUNCTIONS (Module 2.38-2.40)
@st.cache_data
def get_high_risk_customers_sql(threshold=70):
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_high_risk_customers(min_risk_score=threshold)

@st.cache_data  
def get_open_tickets_by_priority_sql(priority=None):
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_open_tickets(priority=priority)

@st.cache_data
def get_dashboard_kpis_sql():
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_dashboard_kpis()

@st.cache_data
def get_revenue_at_risk_sql():
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_revenue_at_risk()

@st.cache_data
def get_ticket_metrics_sql():
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_ticket_metrics()

@st.cache_data
def search_customers_sql(search_term):
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.search_customers(search_term)

@st.cache_data
def get_renewal_pipeline_sql(days_ahead=90):
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_renewal_pipeline(days_ahead=days_ahead)

def inject_custom_css():
    st.markdown("""
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap");
        @import url("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap");

        html, body, p, div, span, a, h1, h2, h3, h4, h5, h6, li, label, .stMarkdown { 
            font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif; 
            color: #1b1b1d; /* on-background */
        }
        
        .material-symbols-outlined {
            font-family: 'Material Symbols Outlined' !important;
            font-weight: normal;
            font-style: normal;
            font-size: 24px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            -webkit-font-smoothing: antialiased;
        }
        
        .main { background-color: #fcf8fa; padding: 2rem; } /* bg-background */
        .stApp { background-color: #fcf8fa; }
        
        /* Sidebar styling to match Stitch */
        [data-testid="stSidebar"] { 
            background-color: #f0edef; /* surface-container */
            border-right: 1px solid #c6c6cd; /* outline-variant */
            padding-top: 1rem; 
            box-shadow: none;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div { color: #45464d !important; }
        [data-testid="stSidebarNav"] a { border-radius: 4px; margin: 4px 12px; }
        [data-testid="stSidebarNav"] a:hover { background-color: #e4e2e4 !important; /* surface-container-highest */ }
        [data-testid="stSidebarNav"] a[aria-current="page"] { 
            background-color: transparent !important; 
            border-right: 4px solid #000000;
            border-radius: 0;
            color: #000000 !important;
            font-weight: 700;
        }
        [data-testid="stSidebarNav"] span { color: #000000 !important; font-weight: 500; font-size: 14px; }
        
        /* Container and Typography */
        .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 100%; }
        footer { display: none; }
        h1 { color: #000000 !important; font-size: 36px !important; font-weight: 700 !important; margin-bottom: 0.5rem !important; line-height: 44px; letter-spacing: -0.02em; }
        h2 { color: #000000 !important; font-size: 24px !important; font-weight: 600 !important; margin-bottom: 1rem !important; line-height: 32px; letter-spacing: -0.01em; }
        h3 { color: #000000 !important; font-size: 20px !important; font-weight: 600 !important; }
        
        /* Cards */
        .metric-card, .content-card { 
            background-color: #ffffff; /* surface-container-lowest */
            border: 1px solid #c6c6cd; /* outline-variant */
            border-radius: 0.5rem; /* rounded-lg */
            padding: 24px; 
            margin-bottom: 16px; 
            box-shadow: none; 
            transition: box-shadow 0.2s; 
        }
        .metric-card:hover, .content-card:hover { 
            box-shadow: 0px 4px 6px -1px rgba(15, 23, 42, 0.1); 
        }
        
        /* Metrics Specific */
        .metric-label { font-size: 12px; color: #45464d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
        .metric-value { font-size: 36px; font-weight: 700; color: #000000; line-height: 44px; font-variant-numeric: tabular-nums; letter-spacing: -0.02em; }
        .metric-change { font-size: 12px; font-weight: 500; margin-top: 8px; }
        .positive { color: #166534; background-color: #DCFCE7; padding: 4px; border-radius: 4px; } 
        .negative { color: #ba1a1a; background-color: #ffdad6; padding: 4px; border-radius: 4px; }
        
        /* Badges */
        .badge { display: inline-block; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 500; }
        .badge-critical { background-color: #ffdad6; color: #ba1a1a; border: 1px solid #ffb4ab; }
        .badge-high { background-color: #ffefd6; color: #ba6a1a; border: 1px solid #ffdfab; }
        .badge-medium { background-color: #f0edef; color: #45464d; border: 1px solid #c6c6cd; }
        .badge-low { background-color: #DCFCE7; color: #166534; border: 1px solid #bbf7d0; }
        
        /* Buttons */
        .btn-primary { background-color: #000000; color: #ffffff; padding: 8px 16px; border-radius: 4px; border: none; font-weight: 500; font-size: 14px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center; gap: 8px; transition: opacity 0.2s; }
        .btn-primary:hover { opacity: 0.9; }
        .btn-secondary { background-color: transparent; color: #45464d; padding: 8px 16px; border-radius: 4px; border: 1px solid #76777d; font-weight: 500; font-size: 14px; text-decoration: none; display: inline-flex; align-items: center; justify-content: center; gap: 8px; transition: background-color 0.2s; }
        .btn-secondary:hover { background-color: #f6f3f5; }
        
        /* Tables */
        .data-table { width: 100%; border-collapse: collapse; }
        .data-table th { text-align: left; padding: 12px; font-size: 12px; font-weight: 600; color: #45464d; border-bottom: 1px solid #c6c6cd; }
        .data-table td { padding: 16px 12px; border-bottom: 1px solid #e4e2e4; font-size: 14px; color: #1b1b1d; }
    </style>

    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("""
        <div style="padding: 0 1rem 2rem 1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 32px; height: 32px; background-color: #1a73e8; border-radius: 6px; 
                            display: flex; align-items: center; justify-content: center; color: white; 
                            font-weight: 700; font-size: 14px;">📊</div>
                <div>
                    <div style="font-size: 16px; font-weight: 700; color: #0F172A;">ChurnGuard AI</div>
                    <div style="font-size: 11px; color: #64748B;">Enterprise Analytics</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)



