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
        background-color: #f5f5f5;
        padding: 2rem;
    }
    
    .stApp {
        background-color: #f5f5f5;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e5e5;
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
        color: #1a1a1a !important;
        font-size: 32px !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #1a1a1a !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        color: #1a1a1a !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    p, span, label, div {
        color: #525252 !important;
    }
    
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .metric-label {
        font-size: 12px;
        color: #737373;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        color: #1a1a1a;
        line-height: 1;
    }
    
    .metric-change {
        font-size: 13px;
        font-weight: 600;
        margin-top: 8px;
    }
    
    .positive { color: #16a34a; }
    .negative { color: #dc2626; }
    
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .badge-critical { background-color: #fee2e2; color: #991b1b; }
    .badge-high { background-color: #fed7aa; color: #9a3412; }
    .badge-medium { background-color: #fef3c7; color: #92400e; }
    .badge-low { background-color: #dbeafe; color: #1e40af; }
    .badge-negative { background-color: #fee2e2; color: #991b1b; }
    
    .content-card {
        background-color: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .btn-primary {
        background-color: #1a1a1a;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        border: none;
        font-weight: 500;
        font-size: 14px;
        text-decoration: none;
        display: inline-block;
    }
    
    .btn-secondary {
        background-color: white;
        color: #1a1a1a;
        padding: 8px 16px;
        border-radius: 6px;
        border: 1px solid #d4d4d4;
        font-weight: 500;
        font-size: 14px;
        text-decoration: none;
        display: inline-block;
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
        font-size: 11px;
        font-weight: 600;
        color: #737373;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid #e5e5e5;
    }
    
    .data-table td {
        padding: 16px 12px;
        border-bottom: 1px solid #f5f5f5;
        font-size: 14px;
        color: #1a1a1a;
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
    np.random.seed(42)
    
    customers = pd.DataFrame({
        'customer_id': range(1, 201),
        'company_name': [f'Company {chr(65 + i % 26)}{i}' for i in range(1, 201)],
        'risk_score': np.random.randint(20, 95, 200),
        'arr': np.random.randint(50000, 5000000, 200),
        'health_status': np.random.choice(['Low Risk', 'Medium', 'Critical'], 200, p=[0.71, 0.17, 0.12]),
        'last_activity': [datetime.now() - timedelta(days=np.random.randint(1, 30)) for _ in range(200)],
        'sentiment': np.random.choice(['Positive', 'Neutral', 'Negative'], 200, p=[0.3, 0.4, 0.3])
    })
    
    subjects_list = ['Data export failing on Q3 Reports Dashboard', 'API timeout issues', 
                     'Dashboard UI glitch', 'Integration error']
    
    tickets = pd.DataFrame({
        'ticket_id': [f'TKT-{2800+i}' for i in range(50)],
        'customer': ['Sarah Jenkins' if i % 3 == 0 else 'John Doe' if i % 3 == 1 else 'Jane Smith' for i in range(50)],
        'company': ['Acme Corp' if i < 10 else 'TechFlow' if i < 20 else 'GlobalNet' for i in range(50)],
        'subject': [subjects_list[i % 4] for i in range(50)],
        'priority': np.random.choice(['Low', 'Medium', 'High', 'Critical'], 50, p=[0.2, 0.4, 0.3, 0.1]),
        'status': np.random.choice(['Open', 'In Progress', 'Awaiting Response', 'Resolved'], 50),
        'risk_score': np.random.randint(30, 95, 50),
        'sentiment': np.random.choice(['Positive', 'Neutral', 'Negative'], 50),
        'created': [datetime.now() - timedelta(hours=np.random.randint(1, 168)) for _ in range(50)]
    })
    
    return customers, tickets

customers_df, tickets_df = load_data()

# PAGE 1: EXECUTIVE DASHBOARD
if page == "Executive Dashboard":
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Executive Insights")
        st.markdown("Real-time overview of churn risk and retention performance.")
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<a href="#" class="btn-secondary">📄 Export Report</a> &nbsp; <a href="#" class="btn-primary">🔍 Filter View</a>', 
                   unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI Cards Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="metric-label">PROJECTED CHURN RATE</div>
                <div style="font-size: 18px;">📉</div>
            </div>
            <div class="metric-value">12.4%</div>
            <div class="metric-change negative">↗ 1.2%</div>
            <div style="font-size: 12px; color: #737373; margin-top: 4px;">vs. last month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="metric-label">REVENUE AT RISK</div>
                <div style="font-size: 18px;">💰</div>
            </div>
            <div class="metric-value">$4.2M</div>
            <div class="metric-change negative">↗ $200k</div>
            <div style="font-size: 12px; color: #737373; margin-top: 4px;">Active High-Risk accounts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div class="metric-label">AVERAGE RISK SCORE</div>
                <div style="font-size: 18px;">📊</div>
            </div>
            <div class="metric-value">68</div>
            <div style="background: #e5e5e5; height: 4px; border-radius: 2px; margin-top: 8px;">
                <div style="background: #1a1a1a; width: 68%; height: 100%;"></div>
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
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        churn_volume = [100, 95, 105, 110, 98, 92]
        preventative = [20, 28, 32, 45, 58, 68]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=months, y=churn_volume, name='Churn Volume', 
                            marker_color='#1a1a1a', text=churn_volume, textposition='inside'))
        fig.add_trace(go.Bar(x=months, y=preventative, name='Preventative Actions', 
                            marker_color='#e5e5e5', text=preventative, textposition='inside'))
        
        fig.update_layout(
            barmode='stack',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#1a1a1a', family='Inter'),
            height=300,
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=40, b=0),
            xaxis=dict(showgrid=False, showline=False),
            yaxis=dict(showgrid=True, gridcolor='#f5f5f5', showline=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Risk Distribution by Segment")
        
        labels = ['Enterprise (High Risk)', 'Mid-Market', 'SMB']
        values = [35, 28, 37]
        colors = ['#dc2626', '#1a1a1a', '#d4d4d4']
        
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
            font=dict(color='#1a1a1a', family='Inter'),
            height=300,
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Top Reasons for Dissatisfaction
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Top Reasons for Dissatisfaction")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        reasons = [
            ('Support Latency', 45),
            ('Feature Gap (Reporting)', 32),
            ('Price / Value Perception', 18)
        ]
        
        for reason, value in reasons:
            st.markdown(f"""
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #1a1a1a; font-weight: 500;">{reason}</span>
                    <span style="color: #1a1a1a; font-weight: 600;">{value}%</span>
                </div>
                <div style="background: #f5f5f5; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: #1a1a1a; width: {value}%; height: 100%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent High-Value Escalations Table
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### Recent High-Value Escalations")
    with col2:
        st.markdown('<div style="text-align: right;"><a href="#" class="btn-secondary">View All</a></div>', 
                   unsafe_allow_html=True)
    
    st.markdown("""
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
            <tr>
                <td><span style="color: #dc2626;">●</span> Global Tech Solutions</td>
                <td>$1.2M / yr</td>
                <td><span class="badge badge-critical">Critical</span></td>
                <td>Pending Exec Review</td>
                <td><a href="#" class="btn-secondary" style="padding: 6px 12px; font-size: 12px;">Intervene</a></td>
            </tr>
            <tr>
                <td><span style="color: #f59e0b;">●</span> Apex Manufacturing</td>
                <td>$850k / yr</td>
                <td><span class="badge badge-high">High</span></td>
                <td>Account Manager Assigned</td>
                <td><a href="#" class="btn-secondary" style="padding: 6px 12px; font-size: 12px;">Review</a></td>
            </tr>
            <tr>
                <td><span style="color: #dc2626;">●</span> Nexus Retail Group</td>
                <td>$620k / yr</td>
                <td><span class="badge badge-critical">Critical</span></td>
                <td>Support Escalation Active</td>
                <td><a href="#" class="btn-secondary" style="padding: 6px 12px; font-size: 12px;">Intervene</a></td>
            </tr>
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
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("""
            <div style="text-align: center;">
                <div style="font-size: 32px; font-weight: 700; color: #16a34a;">142</div>
                <div style="font-size: 11px; color: #737373; text-transform: uppercase;">LOW RISK</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div style="text-align: center;">
                <div style="font-size: 32px; font-weight: 700; color: #f59e0b;">34</div>
                <div style="font-size: 11px; color: #737373; text-transform: uppercase;">MEDIUM</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown("""
            <div style="text-align: center;">
                <div style="font-size: 32px; font-weight: 700; color: #dc2626;">12</div>
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
        
        st.markdown("""
        <div style="padding: 12px; background: #fef2f2; border-left: 3px solid #dc2626; border-radius: 6px; margin-bottom: 12px;">
            <div style="font-weight: 600; color: #1a1a1a; margin-bottom: 4px;">
                📈 Acme Corp risk score jumped to 85.
            </div>
            <div style="font-size: 13px; color: #737373;">Support escalation + negative sentiment</div>
            <div style="font-size: 12px; color: #a3a3a3; margin-top: 4px;">2 mins ago</div>
        </div>
        
        <div style="padding: 12px; background: #fffbeb; border-left: 3px solid #f59e0b; border-radius: 6px; margin-bottom: 12px;">
            <div style="font-weight: 600; color: #1a1a1a; margin-bottom: 4px;">
                👤 Key sponsor at TechFlow departed.
            </div>
            <div style="font-size: 13px; color: #737373;">Relationship risk detected</div>
            <div style="font-size: 12px; color: #a3a3a3; margin-top: 4px;">15 mins ago</div>
        </div>
        
        <div style="padding: 12px; background: #fef2f2; border-left: 3px solid #dc2626; border-radius: 6px;">
            <div style="font-weight: 600; color: #1a1a1a; margin-bottom: 4px;">
                📉 Global Net renewal delayed. Expected MRR drop.
            </div>
            <div style="font-size: 13px; color: #737373;">Contract negotiation stalled</div>
            <div style="font-size: 12px; color: #a3a3a3; margin-top: 4px;">1 hr ago</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # High Risk Accounts Table
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### High Risk Accounts")
    
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
            <tr>
                <td><span style="color: #dc2626;">●</span> Acme Corp</td>
                <td><div style="display: inline-flex; align-items: center; justify-content: center; 
                          width: 40px; height: 40px; border-radius: 50%; background: #fee2e2; 
                          color: #991b1b; font-weight: 700; border: 2px solid #dc2626;">85</div></td>
                <td>$1.2M</td>
                <td>2 days ago</td>
                <td><a href="#" class="btn-primary" style="padding: 6px 16px; font-size: 12px;">Intervene</a></td>
            </tr>
            <tr>
                <td><span style="color: #dc2626;">●</span> Stark Industries</td>
                <td><div style="display: inline-flex; align-items: center; justify-content: center; 
                          width: 40px; height: 40px; border-radius: 50%; background: #fed7aa; 
                          color: #9a3412; font-weight: 700; border: 2px solid #f97316;">78</div></td>
                <td>$4.5M</td>
                <td>5 days ago</td>
                <td><a href="#" class="btn-primary" style="padding: 6px 16px; font-size: 12px;">Intervene</a></td>
            </tr>
            <tr>
                <td><span style="color: #f59e0b;">●</span> Wayne Ent.</td>
                <td><div style="display: inline-flex; align-items: center; justify-content: center; 
                          width: 40px; height: 40px; border-radius: 50%; background: #fef3c7; 
                          color: #92400e; font-weight: 700; border: 2px solid #eab308;">62</div></td>
                <td>$800K</td>
                <td>1 week ago</td>
                <td><a href="#" class="btn-secondary" style="padding: 6px 16px; font-size: 12px;">Review</a></td>
            </tr>
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
    
    # Ticket Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div style="margin-bottom: 16px;">
            <span style="color: #3b82f6; font-weight: 600; font-size: 14px;">TKT-2842</span>
            <span class="badge" style="background: #fee2e2; color: #991b1b; margin-left: 8px;">⚠ SL A: 2h 14m</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="text-align: right;"><span class="badge badge-critical">Bug / Data Export</span></div>', 
                   unsafe_allow_html=True)
    
    # Ticket Title
    st.markdown("### Data export failing on Q3 Reports Dashboard")
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <span style="color: #737373;">👤 Sarah Jenkins (Acme Corp)</span>
        <span style="margin: 0 8px; color: #d4d4d4;">●</span>
        <span style="color: #737373;">🕐 Created: 14:23 PM Today</span>
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
    # Header
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("GlobalTech Inc.")
        st.markdown('<span class="badge" style="background: #dc2626; color: white; font-size: 14px;">⚠️ Churn Risk: High (88)</span>', 
                   unsafe_allow_html=True)
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<a href="#" class="btn-primary" style="padding: 10px 20px;">⚡ Initiate Intervention</a>', 
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
