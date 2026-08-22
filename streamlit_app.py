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
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "ChurnGuard AI - Customer Churn Prevention System"
    }
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
        background-color: #0F172A; /* Deep Navy from Stitch Design */
        border-right: 1px solid #1E293B; /* Dark Slate */
        padding-top: 1rem;
    }
    
    /* Target text inside sidebar to be light colored */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] .st-emotion-cache-16idsys p {
        color: #94A3B8 !important; /* Muted grey */
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #F8FAFC !important; /* White for radio labels */
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
    <div style="padding: 0 1rem 2rem 1rem; border-bottom: 1px solid #1E293B; margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 32px; height: 32px; background-color: #3B82F6; border-radius: 6px; 
                        display: flex; align-items: center; justify-content: center; color: white; 
                        font-weight: 700; font-size: 14px;">📊</div>
            <div>
                <div style="font-size: 16px; font-weight: 700; color: #FFFFFF;">ChurnGuard AI</div>
                <div style="font-size: 11px; color: #94A3B8;">Enterprise Analytics</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Navigation Menu")
    
    # Sync with session state
    if 'page' not in st.session_state:
        st.session_state.page = "Executive Dashboard"
    
    current_index = ["Executive Dashboard", "Risk Command Center", "Ticket Workspace", "Customer Directory", "📤 Data Upload"].index(st.session_state.page) if st.session_state.page in ["Executive Dashboard", "Risk Command Center", "Ticket Workspace", "Customer Directory", "📤 Data Upload"] else 0
    
    page = st.radio(
        "Choose a page:",
        ["Executive Dashboard", "Risk Command Center", "Ticket Workspace", "Customer Directory", "📤 Data Upload"],
        index=current_index,
        key="sidebar_radio"
    )
    
    # Update session state when sidebar changes
    st.session_state.page = page
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("⚙️ **Settings**")
    st.markdown("❓ **Help Support**")

# ========================================
# REAL RISK CALCULATION (Module 2.36)
# Business Logic for Customer Churn Risk Assessment
# ========================================

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
    
    print(f"[SUCCESS] Loaded from database: {len(customers)} customers, {len(tickets)} tickets, {len(interactions)} interactions")
    
    return customers, tickets, interactions, churn_history


customers_df, tickets_df, interactions_df, churn_history_df = load_data()

# Apply real risk calculation to all customers
if not customers_df.empty:
    customers_df['risk_score'] = customers_df.apply(
        lambda row: calculate_real_risk_score(row, tickets_df, interactions_df), 
        axis=1
    )
    customers_df['health_status'] = customers_df['risk_score'].apply(calculate_health_status)
    print(f"[INFO] Risk scores calculated for {len(customers_df)} customers")
    print(f"[INFO] Risk distribution: Critical={len(customers_df[customers_df['health_status']=='Critical'])}, " +
          f"Medium={len(customers_df[customers_df['health_status']=='Medium'])}, " +
          f"Low={len(customers_df[customers_df['health_status']=='Low Risk'])}")



# ========================================
# SQL QUERY FUNCTIONS (Module 2.38-2.40)
# Demonstrates SQL query integration with database
# ========================================

@st.cache_data
def get_high_risk_customers_sql(threshold=70):
    """Get high-risk customers using SQL query from db_queries.py"""
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_high_risk_customers(min_risk_score=threshold)


@st.cache_data  
def get_open_tickets_by_priority_sql(priority=None):
    """Get open tickets by priority using SQL query from db_queries.py"""
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_open_tickets(priority=priority)


@st.cache_data
def get_dashboard_kpis_sql():
    """Get dashboard KPIs using aggregated SQL query from db_queries.py"""
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_dashboard_kpis()


@st.cache_data
def get_revenue_at_risk_sql():
    """Calculate revenue at risk using SQL SUM query from db_queries.py"""
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_revenue_at_risk()


@st.cache_data
def get_ticket_metrics_sql():
    """Get ticket summary metrics using SQL aggregation from db_queries.py"""
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_ticket_metrics()


@st.cache_data
def search_customers_sql(search_term):
    """Search customers using SQL LIKE query from db_queries.py"""
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.search_customers(search_term)


@st.cache_data
def get_renewal_pipeline_sql(days_ahead=90):
    """Get customers with upcoming renewals using SQL date filtering"""
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_renewal_pipeline(days_ahead=days_ahead)


# Add page selector in main area if sidebar is not visible
st.markdown("### 📍 Quick Navigation")
page_col1, page_col2, page_col3, page_col4, page_col5 = st.columns(5)

with page_col1:
    if st.button("📊 Executive Dashboard", use_container_width=True):
        st.session_state.page = "Executive Dashboard"
with page_col2:
    if st.button("🚨 Risk Command Center", use_container_width=True):
        st.session_state.page = "Risk Command Center"
with page_col3:
    if st.button("🎫 Ticket Workspace", use_container_width=True):
        st.session_state.page = "Ticket Workspace"
with page_col4:
    if st.button("👤 Customer Directory", use_container_width=True):
        st.session_state.page = "Customer Directory"
with page_col5:
    if st.button("📤 Data Upload", use_container_width=True):
        st.session_state.page = "📤 Data Upload"

# Get page from session state or default
if 'page' not in st.session_state:
    st.session_state.page = "Executive Dashboard"

# Try to get from sidebar if it exists, otherwise use session state
try:
    page = st.session_state.get('page', "Executive Dashboard")
except:
    page = "Executive Dashboard"

st.markdown("---")

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
    import importlib
    dashboard = importlib.import_module("pages.1_dashboard")
    dashboard.render_dashboard(customers_df, churn_history_df, interactions_df, tickets_df, filter_customers_by_risk)


# PAGE 2: RISK COMMAND CENTER
elif page == "Risk Command Center":
    import importlib
    risk_center = importlib.import_module("pages.2_risk_center")
    risk_center.render_risk_center(customers_df, get_risk_alert_summary)


# PAGE 3: TICKET WORKSPACE
elif page == "Ticket Workspace":
    import importlib
    ticket_workspace = importlib.import_module("pages.3_ticket_workspace")
    ticket_workspace.render_ticket_workspace(tickets_df)


# PAGE 4: CUSTOMER DIRECTORY
elif page == "Customer Directory":
    import importlib
    directory = importlib.import_module("pages.4_directory")
    directory.render_directory(customers_df, export_customer_data)


# PAGE 5: DATA UPLOAD
elif page == "📤 Data Upload":
    st.title("📤 Data Upload & Management")
    st.markdown("Upload CSV files to automatically load customer, ticket, and interaction data into the database.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # SQL QUERY DEMONSTRATION (Module 2.38-2.40)
    # ========================================
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 SQL Query Demonstration")
    st.markdown("**Module 2.38-2.40:** Using `db_queries.py` functions to query the database directly with SQL")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📊 Dashboard KPIs (SQL)**")
        if st.button("Run SQL Query: get_dashboard_kpis()", key="sql_kpis"):
            with st.spinner("Executing SQL query..."):
                kpis = get_dashboard_kpis_sql()
                st.success("✅ SQL Query Executed!")
                st.json(kpis)
    
    with col2:
        st.markdown("**🚨 High Risk Customers (SQL)**")
        threshold = st.slider("Risk Score Threshold:", 0, 100, 70, key="risk_threshold")
        if st.button(f"Run SQL Query: get_high_risk_customers({threshold})", key="sql_high_risk"):
            with st.spinner("Executing SQL query..."):
                high_risk = get_high_risk_customers_sql(threshold)
                st.success(f"✅ Found {len(high_risk)} high-risk customers")
                if not high_risk.empty:
                    st.dataframe(high_risk[['company_name', 'risk_score', 'arr', 'health_status']].head(5))
                else:
                    st.info("No customers above this threshold")
    
    with col3:
        st.markdown("**🎫 Open Tickets (SQL)**")
        priority_filter = st.selectbox("Priority:", [None, "Critical", "High", "Medium", "Low"], key="priority_filter")
        if st.button(f"Run SQL Query: get_open_tickets('{priority_filter}')", key="sql_tickets"):
            with st.spinner("Executing SQL query..."):
                tickets = get_open_tickets_by_priority_sql(priority_filter)
                st.success(f"✅ Found {len(tickets)} open tickets")
                if not tickets.empty:
                    st.dataframe(tickets[['ticket_id', 'priority', 'status', 'company_name']].head(5))
                else:
                    st.info("No open tickets found")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show SQL Query Code
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 💻 SQL Query Examples from `db_queries.py`")
    
    tab1, tab2, tab3 = st.tabs(["Dashboard KPIs", "High Risk Customers", "Open Tickets"])
    
    with tab1:
        st.code('''
# SQL Query for Dashboard KPIs
query = """
SELECT 
    ROUND(AVG(risk_score), 1) as avg_risk_score,
    SUM(CASE WHEN health_status = 'Critical' THEN 1 ELSE 0 END) as critical_customers,
    SUM(CASE WHEN health_status = 'Medium' THEN 1 ELSE 0 END) as medium_customers,
    SUM(CASE WHEN health_status = 'Low Risk' THEN 1 ELSE 0 END) as low_risk_customers,
    SUM(CASE WHEN health_status IN ('Critical', 'Medium') THEN arr ELSE 0 END) as revenue_at_risk,
    SUM(arr) as total_arr,
    COUNT(*) as total_customers
FROM customers
"""
''', language='sql')
    
    with tab2:
        st.code('''
# SQL Query for High Risk Customers
query = """
SELECT * FROM vw_high_risk_customers
WHERE risk_score >= ?
ORDER BY arr DESC
"""
params = (min_risk_score,)
''', language='sql')
    
    with tab3:
        st.code('''
# SQL Query for Open Tickets
query = """
SELECT t.*, c.company_name, c.risk_score as customer_risk
FROM tickets t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.status NOT IN ('Resolved', 'Closed')
AND t.priority = ?
ORDER BY t.created_at DESC
"""
''', language='sql')
    
    st.markdown("</div>", unsafe_allow_html=True)
    
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
