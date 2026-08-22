import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import inject_custom_css, load_data, filter_customers_by_risk

customers_df, tickets_df, interactions_df, churn_history_df = load_data()
inject_custom_css()

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
        prev_actions = interactions_df[interactions_df['interaction_type'].isin(['QBR', 'Call', 'Meeting'])].copy()
        prev_actions['month'] = pd.to_datetime(prev_actions['interaction_date'], errors='coerce').dt.strftime('%b')
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
                        marker_color='#EF4444', text=churn_volume, textposition='inside')) # Stitch Red
    fig.add_trace(go.Bar(x=months, y=preventative, name='Preventative Actions', 
                        marker_color='#3B82F6', text=preventative, textposition='inside')) # Stitch Blue
    
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
    colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#64748B'] # Stitch semantic palette
    
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
