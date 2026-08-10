import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="ChurnGuard AI - Enterprise Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching the exact design screenshots
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .main {
        background-color: #f8fafc; /* Slate 50 */
        padding: 2rem;
    }
    
    .stApp {
        background-color: #f8fafc;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0; /* Slate 200 */
        padding-top: 1rem;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    h1 {
        color: #0F172A !important; /* Deep Navy */
        font-size: 32px !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #0F172A !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        color: #0F172A !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    p, span, label, div {
        color: #475569 !important; /* Slate 600 */
    }
    
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0px 4px 6px -1px rgba(15, 23, 42, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0px 10px 15px -3px rgba(15, 23, 42, 0.1);
    }
    
    .metric-label {
        font-size: 12px;
        color: #64748B; /* Slate 500 */
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        color: #0F172A;
        line-height: 1;
        font-variant-numeric: tabular-nums;
    }
    
    .metric-change {
        font-size: 13px;
        font-weight: 600;
        margin-top: 8px;
    }
    
    .positive { color: #10B981; } /* Emerald */
    .negative { color: #DC2626; } /* Crimson */
    
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .badge-critical { background-color: #fef2f2; color: #DC2626; border: 1px solid #fecaca; }
    .badge-high { background-color: #fffbeb; color: #F59E0B; border: 1px solid #fde68a; }
    .badge-medium { background-color: #f8fafc; color: #64748B; border: 1px solid #e2e8f0; }
    .badge-low { background-color: #ecfdf5; color: #10B981; border: 1px solid #a7f3d0; }
    .badge-negative { background-color: #fef2f2; color: #DC2626; border: 1px solid #fecaca; }
    
    .content-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0px 4px 6px -1px rgba(15, 23, 42, 0.1);
    }
    
    .btn-primary {
        background-color: #0F172A;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        border: none;
        font-weight: 500;
        font-size: 14px;
        text-decoration: none;
        display: inline-block;
        transition: background-color 0.2s;
    }
    
    .btn-primary:hover {
        background-color: #1e293b; /* Slate 800 */
    }
    
    .btn-secondary {
        background-color: white;
        color: #0F172A;
        padding: 8px 16px;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        font-weight: 500;
        font-size: 14px;
        text-decoration: none;
        display: inline-block;
        transition: background-color 0.2s;
    }
    
    .btn-secondary:hover {
        background-color: #f1f5f9; /* Slate 100 */
    }
    
    .stRadio > div > label {
        padding: 10px 16px !important;
        border-radius: 6px !important;
    }
    
    .data-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .data-table th {
        text-align: left;
        padding: 12px;
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .data-table td {
        padding: 16px 12px;
        border-bottom: 1px solid #f8fafc;
        font-size: 14px;
        color: #0F172A;
        font-variant-numeric: tabular-nums;
    }

</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("""
    <div style="padding: 0 1rem 2rem 1rem; border-bottom: 1px solid #e5e5e5; margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 32px; height: 32px; background-color: #1a1a1a; border-radius: 6px; 
                        display: flex; align-items: center; justify-content: center; color: white; 
                        font-weight: 700; font-size: 14px;">📊</div>
            <div>
                <div style="font-size: 16px; font-weight: 700; color: #1a1a1a;">ChurnGuard AI</div>
                <div style="font-size: 11px; color: #737373;">Enterprise Analytics</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["Executive Dashboard", "Risk Command Center", "Ticket Workspace", "Customer Directory", "📤 Data Upload"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("⚙️ **Settings**")
    st.markdown("❓ **Help Support**")

# Load or generate data
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
    
    # Load tickets from database
    tickets = db.execute_query("""
        SELECT t.*, c.company_name, c.risk_score as customer_risk
        FROM tickets t
        JOIN customers c ON t.customer_id = c.customer_id
    """)
    
    # Load interactions from database  
    interactions = db.execute_query("""
        SELECT i.*, c.company_name
        FROM interactions i
        JOIN customers c ON i.customer_id = c.customer_id
    """)
    
    # Create empty churn_history (not in database yet)
    churn_history = pd.DataFrame()
    
    # Add computed columns for compatibility with existing UI
    if not customers.empty:
        customers['arr'] = customers['arr'].astype(float)
        customers['last_activity'] = pd.to_datetime(customers['last_activity'], errors='coerce')
        customers['company_name'] = customers['company_name'].astype(str)
        
    if not tickets.empty:
        tickets['customer'] = 'User ' + tickets['customer_id'].astype(str)
        tickets['company'] = tickets['company_name']
        tickets['risk_score'] = tickets['customer_risk']
    
    print(f"[SUCCESS] Loaded from database: {len(customers)} customers, {len(tickets)} tickets, {len(interactions)} interactions")
    
    return customers, tickets, interactions, churn_history


customers_df, tickets_df, interactions_df, churn_history_df = load_data()

# Function to filter customers by risk level
def filter_customers_by_risk(df, risk_filter):
    """Filter customers based on selected risk levels"""
    if "All Levels" in risk_filter:
        return df
    return df[df['health_status'].isin(risk_filter)]

# Function to calculate churn probability from risk score
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

# Function to generate risk alert summary
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
    
    return alerts_sorted[:10]  # Return top 10 alerts

# Function to export customer data to CSV
def export_customer_data():
    """Export customer data with risk metrics and health status"""
    export_data = customers_df[['customer_id', 'company_name', 'risk_score', 'arr', 'health_status', 'sentiment']].copy()
    export_data['last_activity'] = customers_df['last_activity'].dt.strftime('%Y-%m-%d')
    csv = export_data.to_csv(index=False)
    return csv

# PAGE 1: EXECUTIVE DASHBOARD
if page == "Executive Dashboard":
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Executive Insights")
        st.markdown("Real-time overview of churn risk and retention performance.")
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<a href="#" class="btn-secondary">📄 Export Report</a>', 
                   unsafe_allow_html=True)
    
    # Risk Filter
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([2, 2, 2, 6])
    with col1:
        st.markdown("**🔍 Filter by Risk:**")
    with col2:
        risk_filter = st.multiselect(
            "Risk Level",
            options=["All Levels", "Critical", "Medium", "Low Risk"],
            default=["All Levels"],
            label_visibility="collapsed"
        )
    with col3:
        filtered_customers = filter_customers_by_risk(customers_df, risk_filter)
        st.markdown(f"**Showing {len(filtered_customers)} of {len(customers_df)} customers**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI Cards Row - Dynamic based on filter
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate dynamic metrics with safety checks
    if not filtered_customers.empty and 'arr' in filtered_customers.columns:
        total_arr = filtered_customers['arr'].sum()
    else:
        total_arr = 0
        
    avg_risk = int(filtered_customers['risk_score'].mean()) if not filtered_customers.empty and 'risk_score' in filtered_customers.columns else 0
    
    if not filtered_customers.empty and 'health_status' in filtered_customers.columns:
        critical_count = len(filtered_customers[filtered_customers['health_status'] == 'Critical'])
    else:
        critical_count = 0
        
    churn_rate = (critical_count / len(filtered_customers) * 100) if len(filtered_customers) > 0 else 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="metric-label">PROJECTED CHURN RATE</div>
                <div style="font-size: 18px;">📉</div>
            </div>
            <div class="metric-value">{churn_rate:.1f}%</div>
            <div class="metric-change negative">↗ 1.2%</div>
            <div style="font-size: 12px; color: #737373; margin-top: 4px;">vs. last month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="metric-label">REVENUE AT RISK</div>
                <div style="font-size: 18px;">💰</div>
            </div>
            <div class="metric-value">${total_arr/1000000:.1f}M</div>
            <div class="metric-change negative">↗ $200k</div>
            <div style="font-size: 12px; color: #737373; margin-top: 4px;">{critical_count} High-Risk accounts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="metric-label">AVERAGE RISK SCORE</div>
                <div style="font-size: 18px;">📊</div>
            </div>
            <div class="metric-value">{avg_risk}</div>
            <div style="background: #e5e5e5; height: 4px; border-radius: 2px; margin-top: 8px;">
                <div style="background: #1a1a1a; width: {avg_risk}%; height: 100%;"></div>
            </div>
            <div style="font-size: 12px; color: #737373; margin-top: 4px;">Critical threshold: 75</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="metric-label">RETENTION ROI</div>
                <div style="font-size: 18px;">🎯</div>
            </div>
            <div class="metric-value">+15.8%</div>
            <div class="metric-change positive">↗ 3.4%</div>
            <div style="font-size: 12px; color: #737373; margin-top: 4px;">From active interventions</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Churn Trend vs. Prevention Actions")
        
        # Aggregate churns by month
        if not churn_history_df.empty:
            churn_history_df['month'] = pd.to_datetime(churn_history_df['churn_date']).dt.strftime('%b')
            churn_by_month = churn_history_df.groupby('month').size()
        else:
            churn_by_month = pd.Series()
            
        # Aggregate preventative actions (QBR, Support Call, Executive Review) by month
        if not interactions_df.empty:
            prev_actions = interactions_df[interactions_df['interaction_type'].isin(['QBR', 'Support Call', 'Executive Review'])].copy()
            prev_actions['month'] = pd.to_datetime(prev_actions['interaction_date']).dt.strftime('%b')
            prev_by_month = prev_actions.groupby('month').size()
        else:
            prev_by_month = pd.Series()
            
        # Align months
        all_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        months = [m for m in all_months if m in churn_by_month.index or m in prev_by_month.index][-6:] # Last 6 active months
        if not months:
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            
        churn_volume = [churn_by_month.get(m, 0) for m in months]
        preventative = [prev_by_month.get(m, 0) for m in months]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=months, y=churn_volume, name='Churn Volume', 
                            marker_color='#0F172A', text=churn_volume, textposition='inside'))
        fig.add_trace(go.Bar(x=months, y=preventative, name='Preventative Actions', 
                            marker_color='#94A3B8', text=preventative, textposition='inside'))
        
        fig.update_layout(
            barmode='stack',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#0F172A', family='Inter'),
            height=300,
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=40, b=0),
            xaxis=dict(showgrid=False, showline=False),
            yaxis=dict(showgrid=True, gridcolor='#F1F5F9', showline=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Risk Distribution by Industry")
        
        industry_counts = filtered_customers['industry'].value_counts()
        labels = industry_counts.index.tolist()
        values = industry_counts.values.tolist()
        colors = px.colors.qualitative.Pastel
        
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=.5,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textfont=dict(size=12, family='Inter')
        )])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#0F172A', family='Inter'),
            height=300,
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Top Reasons for Dissatisfaction
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Top Ticket Subjects")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # Get top ticket subjects dynamically
        if not tickets_df.empty:
            top_subjects = tickets_df['subject'].value_counts().head(3)
            total_tickets = len(tickets_df)
            reasons = [(subj, int((count/total_tickets)*100)) for subj, count in top_subjects.items()]
        else:
            reasons = []
            
        for reason, value in reasons:
            st.markdown(f"""
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #0F172A; font-weight: 500;">{reason}</span>
                    <span style="color: #0F172A; font-weight: 600;">{value}%</span>
                </div>
                <div style="background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: #0F172A; width: {value}%; height: 100%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent High-Value Escalations Table
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### High-Value Escalations")
    with col2:
        st.markdown('<div style="text-align: right;"><a href="#" class="btn-secondary">View All</a></div>', 
                   unsafe_allow_html=True)
    
    # Dynamic table
    top_critical = filtered_customers[filtered_customers['health_status'] == 'Critical'].sort_values('arr', ascending=False).head(5)
    
    table_rows = ""
    for _, row in top_critical.iterrows():
        table_rows += f"""
            <tr>
                <td><span style="color: #DC2626;">●</span> {row['company_name']}</td>
                <td>${row['arr']/1000:,.0f}k / yr</td>
                <td><span class="badge badge-critical">Critical</span></td>
                <td>Support Escalation Active</td>
                <td><a href="#" class="btn-secondary" style="padding: 6px 12px; font-size: 12px;">Intervene</a></td>
            </tr>
        """
        
    st.markdown(f"""
    <table class="data-table">
        <thead>
            <tr>
                <th>ACCOUNT NAME</th>
                <th>REVENUE IMPACT</th>
                <th>RISK LEVEL</th>
                <th>CURRENT STATUS</th>
                <th>ACTION</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# PAGE 2: RISK COMMAND CENTER
elif page == "Risk Command Center":
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Risk Command Center")
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<a href="#" class="btn-secondary">🔽 Filter by CSM</a> &nbsp; <a href="#" class="btn-secondary">📤 Export</a>', 
                   unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Summary Cards
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Health Score Summary")
        
        low_count = len(customers_df[customers_df['health_status'] == 'Low Risk'])
        med_count = len(customers_df[customers_df['health_status'] == 'Medium'])
        crit_count = len(customers_df[customers_df['health_status'] == 'Critical'])
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 32px; font-weight: 700; color: #16a34a;">{low_count}</div>
                <div style="font-size: 11px; color: #737373; text-transform: uppercase;">LOW RISK</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 32px; font-weight: 700; color: #f59e0b;">{med_count}</div>
                <div style="font-size: 11px; color: #737373; text-transform: uppercase;">MEDIUM</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 32px; font-weight: 700; color: #dc2626;">{crit_count}</div>
                <div style="font-size: 11px; color: #737373; text-transform: uppercase;">HIGH RISK</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.markdown("### 🚨 Active Risk Alerts")
        with col_b:
            st.markdown('<div style="text-align: right; font-size: 12px; color: #737373;">Live Feed</div>', 
                       unsafe_allow_html=True)
        
        # dynamic alerts based on top critical
        alerts_html = ""
        top_critical_alerts = customers_df[customers_df['health_status'] == 'Critical'].sort_values('risk_score', ascending=False).head(3)
        for _, row in top_critical_alerts.iterrows():
            alerts_html += f"""
            <div style="padding: 12px; background: #fef2f2; border-left: 3px solid #dc2626; border-radius: 6px; margin-bottom: 12px;">
                <div style="font-weight: 600; color: #1a1a1a; margin-bottom: 4px;">
                    📈 {row['company_name']} risk score is {int(row['risk_score'])}.
                </div>
                <div style="font-size: 13px; color: #737373;">Sentiment: {row['sentiment']}</div>
            </div>
            """
            
        st.markdown(alerts_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # NEW: Smart Alert Analysis Panel
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.markdown("### 🔔 Smart Alert Analysis")
    with col_header2:
        if st.button("🔄 Refresh Alerts", key="refresh_alerts"):
            st.rerun()
    
    # Generate dynamic alerts
    alert_list = get_risk_alert_summary(customers_df)
    
    if alert_list:
        # Display alert count by severity
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        critical_count = sum(1 for a in alert_list if a['severity'] == 'Critical')
        high_count = sum(1 for a in alert_list if a['severity'] == 'High')
        medium_count = sum(1 for a in alert_list if a['severity'] == 'Medium')
        
        with col_stat1:
            st.markdown(f"""
            <div style="text-align: center; padding: 12px; background: #fee2e2; border-radius: 6px;">
                <div style="font-size: 28px; font-weight: 700; color: #dc2626;">{critical_count}</div>
                <div style="font-size: 12px; color: #991b1b; font-weight: 600;">Critical Alerts</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            st.markdown(f"""
            <div style="text-align: center; padding: 12px; background: #fed7aa; border-radius: 6px;">
                <div style="font-size: 28px; font-weight: 700; color: #ea580c;">{high_count}</div>
                <div style="font-size: 12px; color: #9a3412; font-weight: 600;">High Priority</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat3:
            st.markdown(f"""
            <div style="text-align: center; padding: 12px; background: #fef3c7; border-radius: 6px;">
                <div style="font-size: 28px; font-weight: 700; color: #ca8a04;">{medium_count}</div>
                <div style="font-size: 12px; color: #92400e; font-weight: 600;">Medium Priority</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display alerts in a table format
        alerts_table = ""
        for alert in alert_list:
            severity_badge = {
                'Critical': '<span class="badge badge-critical">Critical</span>',
                'High': '<span class="badge badge-high">High</span>',
                'Medium': '<span class="badge badge-medium">Medium</span>',
                'Low': '<span class="badge badge-low">Low</span>'
            }
            
            arr_display = f"${alert['arr']/1000000:.1f}M" if alert['arr'] >= 1000000 else f"${alert['arr']/1000:.0f}K"
            
            alerts_table += f"""
            <div style="padding: 16px; border: 1px solid #e5e5e5; border-radius: 8px; margin-bottom: 12px; 
                        background: white; display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                        <span style="font-size: 24px;">{alert['icon']}</span>
                        <div>
                            <div style="font-weight: 600; font-size: 14px; color: #1a1a1a;">{alert['company']}</div>
                            <div style="font-size: 12px; color: #737373;">ARR: {arr_display}</div>
                        </div>
                    </div>
                    <div style="font-size: 13px; color: #525252; margin-bottom: 4px;">
                        <strong>{alert['alert']}</strong>
                    </div>
                    <div style="font-size: 12px; color: #737373;">{alert['detail']}</div>
                </div>
                <div style="text-align: right;">
                    {severity_badge[alert['severity']]}
                    <div style="margin-top: 8px;">
                        <a href="#" class="btn-primary" style="padding: 6px 12px; font-size: 11px; text-decoration: none;">Take Action</a>
                    </div>
                </div>
            </div>
            """
        
        st.markdown(alerts_table, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #737373;">
            <div style="font-size: 48px; margin-bottom: 16px;">✅</div>
            <div style="font-size: 16px; font-weight: 600;">No Critical Alerts</div>
            <div style="font-size: 14px; margin-top: 8px;">All customers are in good standing</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # High Risk Accounts TableLJ
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### High Risk Accounts")
    
    top_accounts = customers_df[customers_df['health_status'].isin(['Critical', 'Medium'])].sort_values('risk_score', ascending=False).head(5)
    account_rows = ""
    for _, row in top_accounts.iterrows():
        color_hex = "#dc2626" if row['health_status'] == 'Critical' else "#f59e0b"
        bg_hex = "#fee2e2" if row['health_status'] == 'Critical' else "#fef3c7"
        text_hex = "#991b1b" if row['health_status'] == 'Critical' else "#92400e"
        border_hex = "#dc2626" if row['health_status'] == 'Critical' else "#eab308"
        action = "Intervene" if row['health_status'] == 'Critical' else "Review"
        btn_class = "btn-primary" if row['health_status'] == 'Critical' else "btn-secondary"
        last_active_str = pd.to_datetime(row['last_activity']).strftime('%b %d, %Y') if pd.notna(row['last_activity']) else "No Activity"
        
        account_rows += f"""
            <tr>
                <td><span style="color: {color_hex};">●</span> {row['company_name']}</td>
                <td><div style="display: inline-flex; align-items: center; justify-content: center; 
                          width: 40px; height: 40px; border-radius: 50%; background: {bg_hex}; 
                          color: {text_hex}; font-weight: 700; border: 2px solid {border_hex};">{int(row['risk_score'])}</div></td>
                <td>${row['arr']/1000:,.0f}K</td>
                <td>{last_active_str}</td>
                <td><a href="#" class="{btn_class}" style="padding: 6px 16px; font-size: 12px;">{action}</a></td>
            </tr>
        """
    
    st.markdown("""
    <table class="data-table">
        <thead>
            <tr>
                <th>ACCOUNT NAME</th>
                <th>RISK SCORE</th>
                <th>REVENUE (ARR)</th>
                <th>LAST ACTIVITY</th>
                <th>ACTION</th>
            </tr>
        </thead>
        <tbody>
            {account_rows}
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# PAGE 3: TICKET WORKSPACE
elif page == "Ticket Workspace":
    # Header with search
    st.title("Ticket Workspace")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.text_input("🔍 Search tickets, accounts, or keywords...", label_visibility="collapsed", 
                     placeholder="Search tickets, accounts, or keywords...")
    with col2:
        st.markdown('<br><a href="#" class="btn-secondary" style="padding: 10px 20px;">✓ Assign</a>', 
                   unsafe_allow_html=True)
    with col3:
        st.markdown('<br><a href="#" class="btn-primary" style="padding: 10px 20px;">Resolve</a>', 
                   unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Ticket Card
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    
    # Dynamic Ticket Selection
    if not tickets_df.empty:
        # Get an open ticket, preferably high/critical priority
        open_tickets = tickets_df[tickets_df['status'].isin(['Open', 'In Progress'])]
        if not open_tickets.empty:
            ticket = open_tickets.sort_values('risk_score', ascending=False).iloc[0]
        else:
            ticket = tickets_df.iloc[0]
            
        tkt_id = ticket['ticket_id']
        tkt_subject = ticket['subject']
        tkt_customer = ticket.get('company', f"Customer {ticket['customer_id']}")
        tkt_priority = ticket['priority']
        tkt_created = pd.to_datetime(ticket['created_at']).strftime('%H:%M %p Today') if pd.notna(ticket['created_at']) else "Unknown"
    else:
        tkt_id = "TKT-2842"
        tkt_subject = "Data export failing on Q3 Reports Dashboard"
        tkt_customer = "Acme Corp"
        tkt_priority = "Critical"
        tkt_created = "14:23 PM Today"
        
    priority_badge_class = "badge-critical" if tkt_priority in ['Critical', 'High'] else "badge-medium"
        
    # Ticket Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style="margin-bottom: 16px;">
            <span style="color: #3b82f6; font-weight: 600; font-size: 14px;">{tkt_id}</span>
            <span class="badge" style="background: #fee2e2; color: #991b1b; margin-left: 8px;">⚠ SLA: 2h 14m</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="text-align: right;"><span class="badge {priority_badge_class}">{tkt_priority}</span></div>', 
                   unsafe_allow_html=True)
    
    # Ticket Title
    st.markdown(f"### {tkt_subject}")
    st.markdown(f"""
    <div style="margin-bottom: 16px;">
        <span style="color: #737373;">👤 User ({tkt_customer})</span>
        <span style="margin: 0 8px; color: #d4d4d4;">●</span>
        <span style="color: #737373;">🕐 Created: {tkt_created}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Conversation Thread
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Customer Message
        st.markdown("""
        <div style="background: #f5f5f5; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
            <div style="display: flex; gap: 12px;">
                <div style="width: 36px; height: 36px; background: #dbeafe; border-radius: 50%; 
                           display: flex; align-items: center; justify-content: center; color: #1e40af; 
                           font-weight: 600; flex-shrink: 0;">SJ</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; margin-bottom: 8px;">Sarah Jenkins</div>
                    <div style="color: #525252; line-height: 1.6;">
                        Hi Support,<br><br>
                        I'm trying to export the Q3 retention reports for our executive review tomorrow, but every 
                        time I click the CSV download button, the system hangs and then gives a 504 Gateway 
                        Timeout error.<br><br>
                        This is extremely time-sensitive. We need this data for a board meeting.<br><br>
                        Thanks,<br>
                        Sarah
                    </div>
                    <div style="margin-top: 12px;">
                        <span style="display: inline-block; padding: 8px 12px; background: white; 
                                   border: 1px solid #d4d4d4; border-radius: 6px; font-size: 12px;">
                            📎 error_screenshot.png
                        </span>
                    </div>
                    <div style="text-align: right; color: #a3a3a3; font-size: 12px; margin-top: 8px;">14:22 PM</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # System Note
        st.markdown("""
        <div style="background: #fafafa; padding: 16px; border-radius: 8px; border-left: 3px solid #737373; margin-bottom: 16px;">
            <div style="display: flex; gap: 12px; align-items: start;">
                <div>🤖</div>
                <div>
                    <div style="font-weight: 600; margin-bottom: 4px;">💬 Internal Note (System)</div>
                    <div style="color: #525252; font-size: 13px;">
                        <strong>Automated Risk Analysis:</strong> Customer sentiment is highly negative. 
                        Account is in Renewal Phase (30 days remaining). Export functionality is a known issue 
                        for large datasets on legacy infrastructure (Ticket #ENG-491).
                    </div>
                    <div style="text-align: right; color: #a3a3a3; font-size: 12px; margin-top: 8px;">14:23 PM</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Agent Response Box
        st.markdown("""
        <div style="background: white; border: 1px solid #d4d4d4; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
            <div style="display: flex; gap: 12px; margin-bottom: 12px;">
                <div style="width: 36px; height: 36px; background: #1a1a1a; border-radius: 50%; 
                           display: flex; align-items: center; justify-content: center; color: white; 
                           font-weight: 600; flex-shrink: 0;">You</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; margin-bottom: 4px;">You (Agent)</div>
                    <div style="color: #a3a3a3; font-size: 12px;">14:45 PM</div>
                </div>
            </div>
            <div style="color: #525252; line-height: 1.6; margin-bottom: 16px;">
                Hi Sarah,<br><br>
                I completely understand the urgency for your board meeting. I'm looking into this 
                immediately. Our engineering team is currently investigating a known timeout issue with 
                exceptionally large data exports.
            </div>
            <div style="border-top: 1px solid #e5e5e5; padding-top: 12px; display: flex; gap: 8px;">
                <button style="padding: 6px 12px; background: white; border: 1px solid #d4d4d4; 
                              border-radius: 4px; cursor: pointer;">B</button>
                <button style="padding: 6px 12px; background: white; border: 1px solid #d4d4d4; 
                              border-radius: 4px; cursor: pointer;">I</button>
                <button style="padding: 6px 12px; background: white; border: 1px solid #d4d4d4; 
                              border-radius: 4px; cursor: pointer;">≡</button>
                <button style="padding: 6px 12px; background: white; border: 1px solid #d4d4d4; 
                              border-radius: 4px; cursor: pointer;">📎</button>
                <button style="padding: 6px 12px; background: white; border: 1px solid #d4d4d4; 
                              border-radius: 4px; cursor: pointer;">😊</button>
            </div>
        </div>
        
        <div style="margin-top: 16px;">
            <input type="text" placeholder="Type your reply or add an internal note..." 
                   style="width: 100%; padding: 12px; border: 1px solid #d4d4d4; border-radius: 6px; 
                          font-size: 14px; font-family: Inter;">
        </div>
        
        <div style="margin-top: 12px; display: flex; justify-content: space-between; align-items: center;">
            <label style="font-size: 13px; color: #737373;">
                <input type="checkbox"> Internal Note
            </label>
            <div style="display: flex; gap: 8px;">
                <a href="#" class="btn-secondary">Save Draft</a>
                <a href="#" class="btn-primary">Send ▶</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Customer 360 Context Panel
        st.markdown('<div class="content-card" style="position: sticky; top: 20px;">', unsafe_allow_html=True)
        st.markdown("### Customer 360 Context")
        
        st.markdown("""
        <div style="text-align: center; padding: 16px 0; border-bottom: 1px solid #e5e5e5;">
            <div style="width: 48px; height: 48px; background: #f5f5f5; border-radius: 50%; 
                       display: flex; align-items: center; justify-content: center; margin: 0 auto 8px; 
                       font-weight: 700; font-size: 18px; color: #1a1a1a;">AC</div>
            <div style="font-weight: 600; color: #1a1a1a;">Acme Corp</div>
            <div style="font-size: 12px; color: #737373;">Enterprise Tier • Tech</div>
        </div>
        
        <div style="padding: 16px 0; border-bottom: 1px solid #e5e5e5;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 16px;">
                <div style="text-align: center;">
                    <div style="font-size: 11px; color: #737373; text-transform: uppercase; margin-bottom: 4px;">Risk Score</div>
                    <div style="font-size: 28px; font-weight: 700; color: #dc2626;">72<span style="font-size: 16px;">/100</span></div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 11px; color: #737373; text-transform: uppercase; margin-bottom: 4px;">ARR</div>
                    <div style="font-size: 28px; font-weight: 700; color: #1a1a1a;">$145k</div>
                </div>
            </div>
            <div style="margin-bottom: 12px;">
                <div style="font-size: 11px; color: #737373; margin-bottom: 4px;">Sentiment</div>
                <span class="badge badge-negative">😟 Negative</span>
            </div>
            <div>
                <div style="font-size: 11px; color: #737373; margin-bottom: 4px;">Renewal Date</div>
                <div style="font-size: 14px; color: #1a1a1a;">Oct 15 (28 days)</div>
            </div>
        </div>
        
        <div style="padding: 16px 0; background: #7f1d1d; margin: 0 -24px; padding: 16px 24px; color: white;">
            <div style="font-weight: 600; margin-bottom: 8px;">⚠️ Active Escalation</div>
            <div style="font-size: 13px; opacity: 0.9;">
                Level 2 - Executive Review Required. Flagged due to repeated core feature failure.
            </div>
        </div>
        
        <div style="padding: 16px 0; background: #dbeafe; margin: 0 -24px; padding: 16px 24px;">
            <div style="font-weight: 600; margin-bottom: 8px; color: #1e40af;">💡 AI RECOMMENDATION</div>
            <div style="font-size: 13px; color: #1e40af;">
                Offer a 1-on-1 strategy call with a Success Manager to address feature friction 
                and bypass standard queue.
            </div>
            <div style="margin-top: 12px;">
                <a href="#" class="btn-secondary" style="width: 100%; text-align: center; display: block;">
                    Draft Invitation
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Recent Interactions")
        
        st.markdown("""
        <div style="margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #e5e5e5;">
            <div style="display: flex; gap: 8px;">
                <div>📝</div>
                <div style="flex: 1;">
                    <div style="font-weight: 500; font-size: 13px; color: #1a1a1a;">NPS Survey Submitted</div>
                    <div style="font-size: 12px; color: #737373;">Score: 4/10 (Detractor)</div>
                    <div style="font-size: 11px; color: #a3a3a3; margin-top: 4px;">2 days ago</div>
                </div>
            </div>
        </div>
        
        <div style="margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #e5e5e5;">
            <div style="display: flex; gap: 8px;">
                <div>✅</div>
                <div style="flex: 1;">
                    <div style="font-weight: 500; font-size: 13px; color: #1a1a1a;">Ticket Resolved</div>
                    <div style="font-size: 12px; color: #737373;">Dashboard UI Glitch</div>
                    <div style="font-size: 11px; color: #a3a3a3; margin-top: 4px;">5 days ago</div>
                </div>
            </div>
        </div>
        
        <div style="margin-bottom: 16px;">
            <div style="display: flex; gap: 8px;">
                <div>📋</div>
                <div style="flex: 1;">
                    <div style="font-weight: 500; font-size: 13px; color: #1a1a1a;">QBR Completed</div>
                    <div style="font-size: 12px; color: #737373;">Attended by VP Eng</div>
                    <div style="font-size: 11px; color: #a3a3a3; margin-top: 4px;">3 weeks ago</div>
                </div>
            </div>
        </div>
        
        <a href="#" style="font-size: 13px; color: #3b82f6; text-decoration: none; font-weight: 500;">
            View Full History →
        </a>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# PAGE 4: CUSTOMER DIRECTORY
elif page == "Customer Directory":
    # Dynamic Customer Profile Selection
    if not customers_df.empty:
        # Get the top critical customer
        critical_customers = customers_df[customers_df['health_status'] == 'Critical'].sort_values('risk_score', ascending=False)
        if not critical_customers.empty:
            cust = critical_customers.iloc[0]
        else:
            cust = customers_df.iloc[0]
            
        cust_name = cust['company_name']
        cust_risk = int(cust['risk_score'])
        cust_arr = cust['arr']
        cust_renewal = pd.to_datetime(cust['renewal_date']).strftime('%b %d') if pd.notna(cust['renewal_date']) else "Unknown"
        cust_industry = cust.get('industry', 'Technology')
        cust_size = cust.get('company_size', 'Enterprise')
    else:
        cust_name = "GlobalTech Inc."
        cust_risk = 88
        cust_arr = 1200000
        cust_renewal = "Oct 15"
        cust_industry = "Financial Technology"
        cust_size = "5,000+ Employees"
        
    arr_display = f"${cust_arr/1000000:.1f}M" if cust_arr >= 1000000 else f"${cust_arr/1000:,.0f}K"
    risk_badge = f'<span class="badge" style="background: #dc2626; color: white; font-size: 14px;">⚠️ Churn Risk: High ({cust_risk})</span>' if cust_risk >= 75 else f'<span class="badge" style="background: #f59e0b; color: white; font-size: 14px;">Medium Risk ({cust_risk})</span>'

    # Header
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title(cust_name)
        st.markdown(risk_badge, unsafe_allow_html=True)
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
        csv_data = export_customer_data()
        st.download_button(
            label="📥 Export Customer Data",
            data=csv_data,
            file_name=f"customer_directory_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="export_customers"
        )
        st.markdown('<a href="#" class="btn-primary" style="padding: 10px 20px; margin-left: 8px;">⚡ Initiate Intervention</a>', 
                   unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Company Info Header
    st.markdown(f"""
    <div class="content-card">
        <div style="display: flex; gap: 16px; align-items: start;">
            <div style="width: 64px; height: 64px; background: #dbeafe; border-radius: 8px; 
                       display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0;">
                🏢
            </div>
            <div style="flex: 1;">
                <div style="display: flex; gap: 24px; flex-wrap: wrap;">
                    <div>
                        <div style="font-size: 11px; color: #737373; margin-bottom: 4px;">🏭 {cust_industry}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #737373; margin-bottom: 4px;">💰 ARR: {arr_display}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #737373; margin-bottom: 4px;">📅 Renewal: {cust_renewal}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Content
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col1:
        # Customer Profile
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Customer Profile")
        
        st.markdown(f"""
        <div style="margin-bottom: 16px;">
            <div style="font-size: 11px; color: #737373; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;">INDUSTRY</div>
            <div style="color: #1a1a1a;">{cust_industry}</div>
        </div>
        
        <div style="margin-bottom: 16px;">
            <div style="font-size: 11px; color: #737373; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;">COMPANY SIZE</div>
            <div style="color: #1a1a1a;">{cust_size if pd.notna(cust_size) else "Unknown"}</div>
        </div>
        
        <div style="margin-bottom: 16px;">
            <div style="font-size: 11px; color: #737373; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;">TENURE</div>
            <div style="color: #1a1a1a;">Active Account</div>
        </div>
        
        <div style="margin-bottom: 16px;">
            <div style="font-size: 11px; color: #737373; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;">KEY STAKEHOLDER</div>
            <div style="color: #1a1a1a;">👤 Key Contact (VP Ops)</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Health Metrics
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Health Metrics")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div style="text-align: center;">
                <div style="font-size: 11px; color: #737373; margin-bottom: 4px;">CSAT Score</div>
                <div style="font-size: 32px; font-weight: 700; color: #dc2626;">2.4</div>
                <div style="font-size: 12px; color: #dc2626;">↓1.2</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div style="text-align: center;">
                <div style="font-size: 11px; color: #737373; margin-bottom: 4px;">Usage (WAU)</div>
                <div style="font-size: 32px; font-weight: 700; color: #dc2626;">1,240</div>
                <div style="font-size: 12px; color: #dc2626;">↓15%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid #e5e5e5;">
            <div style="font-size: 11px; color: #737373; margin-bottom: 4px;">Open Support Tickets</div>
            <div style="font-size: 28px; font-weight: 700; color: #dc2626;">14 
                <span style="font-size: 14px; color: #dc2626;">→4 Critical</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Interaction Timeline
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.markdown("### Interaction Timeline")
        with col_b:
            st.markdown('<div style="text-align: right;"><a href="#" class="btn-secondary" style="padding: 4px 8px; font-size: 12px;">🔽</a></div>', 
                       unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 20px;">
            <div style="display: flex; gap: 12px; margin-bottom: 20px;">
                <div style="width: 36px; height: 36px; background: #fee2e2; border-radius: 8px; 
                           display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">😟</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1a1a1a; margin-bottom: 4px;">Negative Sentiment Detected</div>
                    <div style="font-size: 13px; color: #737373; margin-bottom: 4px;">
                        AI detected high frustration in recent email thread regarding API downtime.
                    </div>
                    <div style="font-size: 12px; color: #a3a3a3;">Today, 10:14 AM</div>
                </div>
            </div>
            
            <div style="display: flex; gap: 12px; margin-bottom: 20px;">
                <div style="width: 36px; height: 36px; background: #f5f5f5; border-radius: 8px; 
                           display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">🎫</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1a1a1a; margin-bottom: 4px;">Ticket #8842 Escalated</div>
                    <div style="font-size: 13px; color: #737373; margin-bottom: 4px;">
                        Subject: "Data Sync Failure" - Clicked to Tier 3 Support. Assigned.
                    </div>
                    <div style="font-size: 12px; color: #a3a3a3;">Yesterday, 3:45 PM</div>
                </div>
            </div>
            
            <div style="display: flex; gap: 12px; margin-bottom: 20px;">
                <div style="width: 36px; height: 36px; background: #e5e5e5; border-radius: 8px; 
                           display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">📉</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1a1a1a; margin-bottom: 4px;">Significant Usage Drop</div>
                    <div style="font-size: 13px; color: #737373; margin-bottom: 4px;">
                        Active users dropped by 22% compared to previous 30-day moving average.
                    </div>
                    <div style="font-size: 12px; color: #a3a3a3;">Oct 2, 2023</div>
                </div>
            </div>
            
            <div style="display: flex; gap: 12px; margin-bottom: 20px;">
                <div style="width: 36px; height: 36px; background: #f5f5f5; border-radius: 8px; 
                           display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">📞</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1a1a1a; margin-bottom: 4px;">Q3 Review Call</div>
                    <div style="font-size: 13px; color: #737373; margin-bottom: 4px;">
                        Standard check-in. Client noted concerns about feature roadmap pacing.
                    </div>
                    <div style="font-size: 12px; color: #a3a3a3;">Sep 15, 2023</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        # Retention Strategy
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Retention Strategy")
        
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <div style="font-size: 11px; color: #737373; text-transform: uppercase; font-weight: 600; margin-bottom: 8px;">
                PRIMARY RISK FACTORS
            </div>
            <ul style="padding-left: 20px; margin: 0; color: #1a1a1a;">
                <li style="margin-bottom: 6px;">Recurring API instability (#8682)</li>
                <li style="margin-bottom: 6px;">Poor sentiment in recent communication</li>
                <li style="margin-bottom: 6px;">Low adoption of new Reporting Module</li>
            </ul>
        </div>
        
        <div style="margin-bottom: 20px;">
            <div style="font-size: 11px; color: #737373; text-transform: uppercase; font-weight: 600; margin-bottom: 8px;">
                RECOMMENDED ACTIONS
            </div>
            <div style="margin-bottom: 12px;">
                <input type="checkbox" id="action1" style="margin-right: 8px;">
                <label for="action1" style="font-size: 13px; color: #1a1a1a;">Schedule Executive Sync</label>
                <div style="font-size: 12px; color: #737373; margin-left: 24px; margin-top: 4px;">
                    Engage Elena Jenkins immediately to discuss API stability roadmap.
                </div>
            </div>
            <div style="margin-bottom: 12px;">
                <input type="checkbox" id="action2" style="margin-right: 8px;">
                <label for="action2" style="font-size: 13px; color: #1a1a1a;">Offer Tech Deep-Dive</label>
                <div style="font-size: 12px; color: #737373; margin-left: 24px; margin-top: 4px;">
                    Propose 1-on-1 session with Solutions Architect to optimize API usage.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Account Team
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Account Team")
        
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: #f5f5f5; 
                   border-radius: 6px; margin-bottom: 12px;">
            <div style="width: 36px; height: 36px; background: #dbeafe; border-radius: 50%; 
                       display: flex; align-items: center; justify-content: center; font-weight: 600; 
                       color: #1e40af; flex-shrink: 0;">SM</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 13px; color: #1a1a1a;">Sarah Miller</div>
                <div style="font-size: 12px; color: #737373;">Customer Success Mgr</div>
            </div>
            <div>✉️</div>
        </div>
        
        <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: #f5f5f5; 
                   border-radius: 6px; margin-bottom: 12px;">
            <div style="width: 36px; height: 36px; background: #fef3c7; border-radius: 50%; 
                       display: flex; align-items: center; justify-content: center; font-weight: 600; 
                       color: #92400e; flex-shrink: 0;">DR</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 13px; color: #1a1a1a;">David Rossi</div>
                <div style="font-size: 12px; color: #737373;">Account Executive</div>
            </div>
            <div>✉️</div>
        </div>
        
        <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: #f5f5f5; 
                   border-radius: 6px;">
            <div style="width: 36px; height: 36px; background: #d1fae5; border-radius: 50%; 
                       display: flex; align-items: center; justify-content: center; font-weight: 600; 
                       color: #065f46; flex-shrink: 0;">KL</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 13px; color: #1a1a1a;">Kevin Lee</div>
                <div style="font-size: 12px; color: #737373;">Tier 3 Support Lead</div>
            </div>
            <div>✉️</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# PAGE 5: DATA UPLOAD
elif page == "📤 Data Upload":
    st.title("📤 Data Upload & Management")
    st.markdown("Upload CSV files to automatically load customer, ticket, and interaction data into the database.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Instructions
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📋 How to Upload Data")
    st.markdown("""
    **Step 1:** Prepare your CSV files with the correct format  
    **Step 2:** Upload files using the file uploaders below  
    **Step 3:** Preview the data to verify it looks correct  
    **Step 4:** Click "Load to Database" to import the data  
    
    ---
    
    **Required CSV Formats:**
    - **customers.csv**: customer_id, company_name, industry, arr, contract_type, renewal_date, csm_name
    - **tickets.json**: ticket_id, customer_id, subject, priority, status, sentiment, created_date, resolved_date
    - **interactions.csv**: interaction_id, customer_id, interaction_type, description, timestamp
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # File uploaders
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Upload Customers CSV")
        customers_file = st.file_uploader("Choose customers CSV file", type=['csv'], key="customers_upload")
        
        if customers_file is not None:
            import io
            customers_uploaded = pd.read_csv(customers_file)
            st.success(f"✅ Loaded {len(customers_uploaded)} customers")
            st.dataframe(customers_uploaded.head(), use_container_width=True)
            
            if st.button("💾 Load Customers to Database", key="load_customers"):
                from db_queries import ChurnGuardDB
                import sqlite3
                
                conn = sqlite3.connect('churnguard.db')
                cursor = conn.cursor()
                
                try:
                    # Clear existing customers
                    cursor.execute("DELETE FROM customers")
                    
                    # Insert new customers
                    for _, row in customers_uploaded.iterrows():
                        cursor.execute("""
                            INSERT INTO customers (
                                company_name, industry, arr, 
                                renewal_date, health_status, risk_score, sentiment
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            row['company_name'],
                            row['industry'],
                            int(row['arr']),
                            row['renewal_date'],
                            'Low Risk',
                            20,
                            'Neutral'
                        ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"🎉 Successfully loaded {len(customers_uploaded)} customers into database!")
                    st.info("🔄 Refresh the page to see updated data in dashboards")
                    
                    # Clear cache to reload data
                    st.cache_data.clear()
                    
                except Exception as e:
                    st.error(f"❌ Error loading customers: {str(e)}")
                    conn.close()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🎫 Upload Tickets JSON")
        tickets_file = st.file_uploader("Choose tickets JSON file", type=['json'], key="tickets_upload")
        
        if tickets_file is not None:
            import json
            import io
            tickets_uploaded = json.load(tickets_file)
            tickets_df_uploaded = pd.DataFrame(tickets_uploaded)
            st.success(f"✅ Loaded {len(tickets_df_uploaded)} tickets")
            st.dataframe(tickets_df_uploaded.head(), use_container_width=True)
            
            if st.button("💾 Load Tickets to Database", key="load_tickets"):
                from db_queries import ChurnGuardDB
                import sqlite3
                
                conn = sqlite3.connect('churnguard.db')
                cursor = conn.cursor()
                
                try:
                    # Clear existing tickets
                    cursor.execute("DELETE FROM tickets")
                    
                    # Insert tickets
                    for ticket in tickets_uploaded:
                        # Map customer_id
                        cust_id_str = ticket['customer_id']
                        if isinstance(cust_id_str, str) and 'CUST-' in cust_id_str:
                            cust_id = int(cust_id_str.replace('CUST-', ''))
                        else:
                            cust_id = 1
                        
                        cursor.execute("""
                            INSERT INTO tickets (
                                ticket_id, customer_id, subject, description,
                                priority, status, sentiment, category,
                                created_at, resolved_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            ticket['ticket_id'],
                            cust_id,
                            ticket['subject'],
                            ticket.get('subject', 'No description'),
                            ticket['priority'],
                            ticket['status'],
                            ticket['sentiment'],
                            'Support',
                            ticket['created_date'],
                            ticket.get('resolved_date')
                        ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"🎉 Successfully loaded {len(tickets_uploaded)} tickets into database!")
                    st.info("🔄 Refresh the page to see updated data in dashboards")
                    
                    # Clear cache
                    st.cache_data.clear()
                    
                except Exception as e:
                    st.error(f"❌ Error loading tickets: {str(e)}")
                    conn.close()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactions upload (full width)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 💬 Upload Interactions CSV")
    interactions_file = st.file_uploader("Choose interactions CSV file", type=['csv'], key="interactions_upload")
    
    if interactions_file is not None:
        interactions_uploaded = pd.read_csv(interactions_file)
        st.success(f"✅ Loaded {len(interactions_uploaded)} interactions")
        
        col_preview, col_button = st.columns([3, 1])
        with col_preview:
            st.dataframe(interactions_uploaded.head(10), use_container_width=True)
        
        with col_button:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("💾 Load Interactions to Database", key="load_interactions"):
                from db_queries import ChurnGuardDB
                import sqlite3
                
                conn = sqlite3.connect('churnguard.db')
                cursor = conn.cursor()
                
                try:
                    # Clear existing interactions
                    cursor.execute("DELETE FROM interactions")
                    
                    # Insert interactions
                    for _, row in interactions_uploaded.iterrows():
                        # Map customer_id
                        cust_id_str = row['customer_id']
                        if isinstance(cust_id_str, str) and 'CUST-' in cust_id_str:
                            cust_id = int(cust_id_str.replace('CUST-', ''))
                        else:
                            cust_id = 1
                        
                        # Map interaction types
                        interaction_type = row['interaction_type']
                        type_mapping = {
                            'Login': 'Email',
                            'Feature Usage': 'Training',
                            'Support Call': 'Call',
                            'QBR': 'QBR',
                            'Email Sent': 'Email'
                        }
                        mapped_type = type_mapping.get(interaction_type, 'Email')
                        
                        cursor.execute("""
                            INSERT INTO interactions (
                                customer_id, interaction_type,
                                interaction_date, notes
                            ) VALUES (?, ?, ?, ?)
                        """, (
                            cust_id,
                            mapped_type,
                            row['timestamp'],
                            row['description']
                        ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"🎉 Successfully loaded {len(interactions_uploaded)} interactions into database!")
                    st.info("🔄 Refresh the page to see updated data in dashboards")
                    
                    # Clear cache
                    st.cache_data.clear()
                    
                except Exception as e:
                    st.error(f"❌ Error loading interactions: {str(e)}")
                    conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Current database status
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Current Database Status")
    
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        customer_count = db.execute_query("SELECT COUNT(*) as count FROM customers")['count'][0]
        st.metric("Customers in Database", customer_count)
    
    with col2:
        ticket_count = db.execute_query("SELECT COUNT(*) as count FROM tickets")['count'][0]
        st.metric("Tickets in Database", ticket_count)
    
    with col3:
        interaction_count = db.execute_query("SELECT COUNT(*) as count FROM interactions")['count'][0]
        st.metric("Interactions in Database", interaction_count)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Download sample templates
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📥 Download Sample Templates")
    st.markdown("Need help with the CSV format? Download these sample templates:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sample_customers = pd.DataFrame({
            'customer_id': ['CUST-1001', 'CUST-1002'],
            'company_name': ['Acme Corp', 'TechStart Inc'],
            'industry': ['Tech', 'Finance'],
            'arr': [250000, 150000],
            'contract_type': ['Annual', 'Monthly'],
            'renewal_date': ['2026-12-31', '2026-11-30'],
            'csm_name': ['Alice', 'Bob']
        })
        csv_customers = sample_customers.to_csv(index=False)
        st.download_button(
            label="📄 Download customers.csv",
            data=csv_customers,
            file_name="sample_customers.csv",
            mime="text/csv"
        )
    
    with col2:
        st.markdown("**tickets.json template**")
        st.code('''[
  {
    "ticket_id": "TKT-001",
    "customer_id": "CUST-1001",
    "subject": "API timeout",
    "priority": "High",
    "status": "Open",
    "sentiment": "Negative",
    "created_date": "2026-08-01T10:00:00",
    "resolved_date": null
  }
]''', language='json')
    
    with col3:
        sample_interactions = pd.DataFrame({
            'interaction_id': ['INT-5001', 'INT-5002'],
            'customer_id': ['CUST-1001', 'CUST-1002'],
            'interaction_type': ['QBR', 'Support Call'],
            'description': ['Quarterly review', 'Technical support'],
            'timestamp': ['2026-08-01 14:00:00', '2026-08-02 10:30:00']
        })
        csv_interactions = sample_interactions.to_csv(index=False)
        st.download_button(
            label="📄 Download interactions.csv",
            data=csv_interactions,
            file_name="sample_interactions.csv",
            mime="text/csv"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
