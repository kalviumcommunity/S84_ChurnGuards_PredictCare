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
        ["Executive Dashboard", "Risk Command Center", "Ticket Workspace", "Customer Directory"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("⚙️ **Settings**")
    st.markdown("❓ **Help Support**")

# Load or generate data
@st.cache_data
def load_data():
    from scripts.data_ingestion import load_data as load_raw
    from scripts.data_cleaning import clean_data
    from scripts.feature_engineering import engineer_features
    
    customers, tickets, interactions, churn_history = load_raw('data')
    customers, tickets, interactions, churn_history = clean_data(customers, tickets, interactions, churn_history)
    customers, tickets = engineer_features(customers, tickets, interactions)
    
    return customers, tickets, interactions, churn_history


customers_df, tickets_df, interactions_df, churn_history_df = load_data()

# Function to filter customers by risk level
def filter_customers_by_risk(df, risk_filter):
    """Filter customers based on selected risk levels"""
    if "All Levels" in risk_filter:
        return df
    return df[df['health_status'].isin(risk_filter)]

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
    
    # Calculate dynamic metrics
    total_arr = filtered_customers['arr'].sum()
    avg_risk = int(filtered_customers['risk_score'].mean()) if not filtered_customers.empty else 0
    critical_count = len(filtered_customers[filtered_customers['health_status'] == 'Critical'])
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
            prev_actions['month'] = pd.to_datetime(prev_actions['timestamp']).dt.strftime('%b')
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
    
    # High Risk Accounts Table
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
        
        account_rows += f"""
            <tr>
                <td><span style="color: {color_hex};">●</span> {row['company_name']}</td>
                <td><div style="display: inline-flex; align-items: center; justify-content: center; 
                          width: 40px; height: 40px; border-radius: 50%; background: {bg_hex}; 
                          color: {text_hex}; font-weight: 700; border: 2px solid {border_hex};">{int(row['risk_score'])}</div></td>
                <td>${row['arr']/1000:,.0f}K</td>
                <td>{pd.to_datetime(row['last_activity']).strftime('%b %d, %Y')}</td>
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
    
    # Select an open ticket dynamically
    open_tickets = tickets_df[tickets_df['status'] == 'Open']
    if open_tickets.empty:
        st.warning("No open tickets at the moment.")
    else:
        with col1:
            ticket_options = open_tickets['ticket_id'].tolist()
            ticket_display = {t_id: f"{t_id} - {open_tickets[open_tickets['ticket_id']==t_id].iloc[0]['subject']}" for t_id in ticket_options}
            selected_ticket_id = st.selectbox("🔍 Select Open Ticket", ticket_options, format_func=lambda x: ticket_display[x], label_visibility="collapsed")
            
        selected_ticket = open_tickets[open_tickets['ticket_id'] == selected_ticket_id].iloc[0]
        customer = customers_df[customers_df['customer_id'] == selected_ticket['customer_id']].iloc[0]
        
        with col2:
            st.markdown('<br><a href="#" class="btn-secondary" style="padding: 10px 20px;">✓ Assign</a>', 
                       unsafe_allow_html=True)
        with col3:
            st.markdown('<br><a href="#" class="btn-primary" style="padding: 10px 20px;">Resolve</a>', 
                       unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Ticket Card
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        # Ticket Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div style="margin-bottom: 16px;">
                <span style="color: #3b82f6; font-weight: 600; font-size: 14px;">{selected_ticket_id}</span>
                <span class="badge" style="background: #fee2e2; color: #991b1b; margin-left: 8px;">⚠ High Priority</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="text-align: right;"><span class="badge badge-critical">{selected_ticket["category"]}</span></div>', 
                       unsafe_allow_html=True)
        
        # Ticket Title
        st.markdown(f"### {selected_ticket['subject']}")
        created_time = pd.to_datetime(selected_ticket['created_at']).strftime('%H:%M %p')
        st.markdown(f"""
        <div style="margin-bottom: 16px;">
            <span style="color: #737373;">👤 Contact ({customer['company_name']})</span>
            <span style="margin: 0 8px; color: #d4d4d4;">●</span>
            <span style="color: #737373;">🕐 Created: {created_time} Today</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Conversation Thread
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # Customer Message
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                <div style="display: flex; gap: 12px;">
                    <div style="width: 36px; height: 36px; background: #dbeafe; border-radius: 50%; 
                               display: flex; align-items: center; justify-content: center; color: #1e40af; 
                               font-weight: 600; flex-shrink: 0;">CT</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; margin-bottom: 8px;">Customer Contact</div>
                        <div style="color: #475569; line-height: 1.6;">
                            {selected_ticket['description']}
                        </div>
                        <div style="text-align: right; color: #94a3b8; font-size: 12px; margin-top: 8px;">{created_time}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # System Note
            st.markdown(f"""
            <div style="background: #f1f5f9; padding: 16px; border-radius: 8px; border-left: 3px solid #64748b; margin-bottom: 16px;">
                <div style="display: flex; gap: 12px; align-items: start;">
                    <div>🤖</div>
                    <div>
                        <div style="font-weight: 600; margin-bottom: 4px;">💬 Internal Note (System)</div>
                        <div style="color: #475569; font-size: 13px;">
                            <strong>Automated Risk Analysis:</strong> Customer sentiment is <b>{selected_ticket['sentiment']}</b>. 
                            Account health is {customer['health_status']}.
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Agent Response Box
            st.markdown("""
            <div style="background: white; border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                <div style="margin-top: 16px;">
                    <input type="text" placeholder="Type your reply or add an internal note..." 
                           style="width: 100%; padding: 12px; border: 1px solid #cbd5e1; border-radius: 6px; 
                                  font-size: 14px; font-family: Inter;">
                </div>
                
                <div style="margin-top: 12px; display: flex; justify-content: space-between; align-items: center;">
                    <label style="font-size: 13px; color: #64748b;">
                        <input type="checkbox"> Internal Note
                    </label>
                    <div style="display: flex; gap: 8px;">
                        <a href="#" class="btn-secondary">Save Draft</a>
                        <a href="#" class="btn-primary">Send ▶</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Customer 360 Context Panel
            st.markdown('<div class="content-card" style="position: sticky; top: 20px;">', unsafe_allow_html=True)
            st.markdown("### Customer 360 Context")
            
            st.markdown(f"""
            <div style="text-align: center; padding: 16px 0; border-bottom: 1px solid #e2e8f0;">
                <div style="font-weight: 600; color: #0F172A; font-size: 18px;">{customer['company_name']}</div>
                <div style="font-size: 12px; color: #64748B;">{customer['industry']}</div>
            </div>
            
            <div style="padding: 16px 0; border-bottom: 1px solid #e2e8f0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 16px;">
                    <div style="text-align: center;">
                        <div style="font-size: 11px; color: #64748B; text-transform: uppercase; margin-bottom: 4px;">Risk Score</div>
                        <div style="font-size: 28px; font-weight: 700; color: #DC2626;">{int(customer['risk_score'])}<span style="font-size: 16px;">/100</span></div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 11px; color: #64748B; text-transform: uppercase; margin-bottom: 4px;">ARR</div>
                        <div style="font-size: 28px; font-weight: 700; color: #0F172A;">${customer['arr']/1000:,.0f}k</div>
                    </div>
                </div>
                <div style="margin-bottom: 12px;">
                    <div style="font-size: 11px; color: #64748B; margin-bottom: 4px;">Sentiment</div>
                    <span class="badge badge-negative">{customer['sentiment']}</span>
                </div>
                <div>
                    <div style="font-size: 11px; color: #64748B; margin-bottom: 4px;">Renewal Date</div>
                    <div style="font-size: 14px; color: #0F172A;">{pd.to_datetime(customer['last_activity']).strftime('%b %d, %Y')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)


# PAGE 4: CUSTOMER DIRECTORY
elif page == "Customer Directory":
    # Header
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("GlobalTech Inc.")
        st.markdown('<span class="badge" style="background: #dc2626; color: white; font-size: 14px;">⚠️ Churn Risk: High (88)</span>', 
                   unsafe_allow_html=True)
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
    st.markdown("""
    <div class="content-card">
        <div style="display: flex; gap: 16px; align-items: start;">
            <div style="width: 64px; height: 64px; background: #dbeafe; border-radius: 8px; 
                       display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0;">
                🏢
            </div>
            <div style="flex: 1;">
                <div style="display: flex; gap: 24px; flex-wrap: wrap;">
                    <div>
                        <div style="font-size: 11px; color: #737373; margin-bottom: 4px;">🏭 Enterprise SaaS</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #737373; margin-bottom: 4px;">💰 ARR: $1.2M</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #737373; margin-bottom: 4px;">📅 Renewal: Oct 15</div>
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
        
        st.markdown("""
        <div style="margin-bottom: 16px;">
            <div style="font-size: 11px; color: #737373; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;">INDUSTRY</div>
            <div style="color: #1a1a1a;">Financial Technology</div>
        </div>
        
        <div style="margin-bottom: 16px;">
            <div style="font-size: 11px; color: #737373; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;">COMPANY SIZE</div>
            <div style="color: #1a1a1a;">5,000+ Employees</div>
        </div>
        
        <div style="margin-bottom: 16px;">
            <div style="font-size: 11px; color: #737373; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;">TENURE</div>
            <div style="color: #1a1a1a;">3 Years, 4 Months</div>
        </div>
        
        <div style="margin-bottom: 16px;">
            <div style="font-size: 11px; color: #737373; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;">KEY STAKEHOLDER</div>
            <div style="color: #1a1a1a;">👤 Elena Jenkins, VP Ops</div>
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
