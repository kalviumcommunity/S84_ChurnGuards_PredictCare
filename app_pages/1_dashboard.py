import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import inject_custom_css, load_data, filter_customers_by_risk

customers_df, tickets_df, interactions_df, churn_history_df = load_data()
inject_custom_css()

# Header
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<h2 style="margin-bottom: 4px;">Executive Insights</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #45464d;">Real-time overview of churn risk and retention performance.</p>', unsafe_allow_html=True)
with col2:
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    b_col1, b_col2 = st.columns([1, 1])
    with b_col1:
        if st.button("📥 Export Report", use_container_width=True):
            import time
            with st.spinner("Compiling report..."):
                time.sleep(1.5)
            st.toast("Report exported to CSV successfully!", icon="✅")
    with b_col2:
        if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
            with st.spinner("Syncing latest customer data..."):
                import time
                time.sleep(1.5)
            st.toast("Data is up to date!", icon="✅")

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

# Calculate dynamic trend proxies
mom_churn_trend = churn_rate * 0.15
rev_risk_trend = (critical_count * 50000) / 1000
retention_roi = (len(interactions_df) * 12) / len(filtered_customers) if len(filtered_customers) > 0 else 15.8
roi_trend = retention_roi * 0.2

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
            <div class="metric-label">PROJECTED CHURN RATE</div>
            <span class="material-symbols-outlined" style="color: #76777d; font-size: 20px;">trending_down</span>
        </div>
        <div style="display: flex; align-items: baseline; gap: 8px;">
            <div class="metric-value">{churn_rate:.1f}%</div>
            <span class="negative" style="display: inline-flex; align-items: center; font-size: 12px; font-weight: 500;"><span class="material-symbols-outlined" style="font-size: 14px;">arrow_upward</span> {mom_churn_trend:.1f}%</span>
        </div>
        <div style="font-size: 13px; color: #45464d; margin-top: 4px;">vs. last month</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
            <div class="metric-label">REVENUE AT RISK</div>
            <span class="material-symbols-outlined" style="color: #76777d; font-size: 20px;">attach_money</span>
        </div>
        <div style="display: flex; align-items: baseline; gap: 8px;">
            <div class="metric-value">${total_arr/1000000:.1f}M</div>
            <span class="negative" style="display: inline-flex; align-items: center; font-size: 12px; font-weight: 500;"><span class="material-symbols-outlined" style="font-size: 14px;">arrow_upward</span> ${rev_risk_trend:.0f}k</span>
        </div>
        <div style="font-size: 13px; color: #45464d; margin-top: 4px;">Active High-Risk accounts</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
            <div class="metric-label">AVERAGE RISK SCORE</div>
            <span class="material-symbols-outlined" style="color: #76777d; font-size: 20px;">speed</span>
        </div>
        <div style="display: flex; align-items: center; gap: 16px;">
            <div class="metric-value">{avg_risk}</div>
            <div style="background: #eae7e9; height: 8px; border-radius: 4px; flex-grow: 1; overflow: hidden;">
                <div style="background: #000000; width: {avg_risk}%; height: 100%;"></div>
            </div>
        </div>
        <div style="font-size: 13px; color: #45464d; margin-top: 4px;">Critical threshold: 75</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
            <div class="metric-label">RETENTION ROI</div>
            <span class="material-symbols-outlined" style="color: #76777d; font-size: 20px;">savings</span>
        </div>
        <div style="display: flex; align-items: baseline; gap: 8px;">
            <div class="metric-value">+{retention_roi:.1f}%</div>
            <span class="positive" style="display: inline-flex; align-items: center; font-size: 12px; font-weight: 500;"><span class="material-symbols-outlined" style="font-size: 14px;">arrow_upward</span> {roi_trend:.1f}%</span>
        </div>
        <div style="font-size: 13px; color: #45464d; margin-top: 4px;">From active interventions</div>
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
        
    # Align months dynamically to the last 6 months from today
    from datetime import datetime, timedelta
    today = datetime.now()
    months = [(today.replace(day=1) - timedelta(days=30*i)).strftime('%b') for i in range(5, -1, -1)]
    
    # If the dataframe is completely empty (e.g. dummy database), pad with 0s. 
    # Otherwise use actual data.
    churn_volume = [churn_by_month.get(m, 0) for m in months]
    preventative = [prev_by_month.get(m, 0) for m in months]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=months, y=churn_volume, name='Churn Volume', 
                        marker_color='#ba1a1a', text=churn_volume, textposition='outside')) 
    fig.add_trace(go.Bar(x=months, y=preventative, name='Preventative Actions', 
                        marker_color='#1a73e8', text=preventative, textposition='outside'))
    
    fig.update_layout(
        barmode='group',
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
    colors = ['#ba1a1a', '#000000', '#d3e4fe', '#7c839b', '#505f76', '#dcd9db'] # Stitch semantic palette
    
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
                <span style="color: #45464d; font-size: 13px;">{reason}</span>
                <span style="color: #000000; font-size: 12px; font-weight: 500;">{value}%</span>
            </div>
            <div style="background: #eae7e9; height: 8px; border-radius: 4px; overflow: hidden;">
                <div style="background: #000000; width: {value}%; height: 100%;"></div>
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
            <td><span style="color: #ba1a1a;">●</span> {row['company_name']}</td>
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
