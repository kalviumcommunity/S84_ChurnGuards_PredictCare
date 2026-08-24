import streamlit as st
import pandas as pd
from utils.data_loader import inject_custom_css, load_data, get_risk_alert_summary

customers_df, tickets_df, interactions_df, churn_history_df = load_data()
inject_custom_css()

# Header
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<h2 style="margin-bottom: 4px;">Risk Command Center</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #45464d;">Monitor and manage customer risk alerts across your portfolio.</p>', unsafe_allow_html=True)
with col2:
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    b_col1, b_col2 = st.columns([1, 1])
    with b_col1:
        if st.button("👥 Filter by CSM", use_container_width=True):
            st.toast("CSM Filter activated (Demo)", icon="ℹ️")
    with b_col2:
        if st.button("📥 Export", type="primary", use_container_width=True):
            import time
            with st.spinner("Preparing export..."):
                time.sleep(1)
            st.toast("Risk alerts exported!", icon="✅")

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
        <div style="text-align: center; padding: 16px; border: 1px solid #ffb4ab; border-radius: 8px; background: #ffdad6;">
            <div style="font-size: 36px; font-weight: 700; color: #ba1a1a;">{crit_count}</div>
            <div style="font-size: 12px; font-weight: 600; color: #ba1a1a; text-transform: uppercase;">HIGH RISK</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div style="text-align: center; padding: 16px; border: 1px solid #ffdfab; border-radius: 8px; background: #ffefd6;">
            <div style="font-size: 36px; font-weight: 700; color: #ba6a1a;">{med_count}</div>
            <div style="font-size: 12px; font-weight: 600; color: #ba6a1a; text-transform: uppercase;">MEDIUM</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""
        <div style="text-align: center; padding: 16px; border: 1px solid #bbf7d0; border-radius: 8px; background: #DCFCE7;">
            <div style="font-size: 36px; font-weight: 700; color: #166534;">{low_count}</div>
            <div style="font-size: 12px; font-weight: 600; color: #166534; text-transform: uppercase;">LOW RISK</div>
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
        <div style="padding: 12px; background: #ffffff; border-left: 4px solid #ba1a1a; border-radius: 6px; border-top: 1px solid #c6c6cd; border-right: 1px solid #c6c6cd; border-bottom: 1px solid #c6c6cd; margin-bottom: 12px; display: flex; gap: 12px;">
            <span class="material-symbols-outlined" style="color: #ba1a1a;">trending_up</span>
            <div>
                <div style="font-weight: 400; color: #1b1b1d; margin-bottom: 4px; font-size: 14px;">
                    <strong>{row['company_name']}</strong> risk score is <strong style="color: #ba1a1a;">{int(row['risk_score'])}</strong>.
                </div>
                <div style="font-size: 12px; color: #45464d;">Sentiment: {row['sentiment']}</div>
            </div>
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
        <div style="text-align: center; padding: 12px; border: 1px solid #ffb4ab; background: #ffdad6; border-radius: 6px;">
            <div style="font-size: 28px; font-weight: 700; color: #ba1a1a;">{critical_count}</div>
            <div style="font-size: 12px; color: #ba1a1a; font-weight: 600; text-transform: uppercase;">Critical Alerts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f"""
        <div style="text-align: center; padding: 12px; border: 1px solid #ffdfab; background: #ffefd6; border-radius: 6px;">
            <div style="font-size: 28px; font-weight: 700; color: #ba6a1a;">{high_count}</div>
            <div style="font-size: 12px; color: #ba6a1a; font-weight: 600; text-transform: uppercase;">High Priority</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown(f"""
        <div style="text-align: center; padding: 12px; border: 1px solid #c6c6cd; background: #f0edef; border-radius: 6px;">
            <div style="font-size: 28px; font-weight: 700; color: #45464d;">{medium_count}</div>
            <div style="font-size: 12px; color: #45464d; font-weight: 600; text-transform: uppercase;">Medium Priority</div>
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
        
        alerts_table += f'''
        <div style="padding: 16px; border: 1px solid #e5e5e5; border-radius: 8px; margin-bottom: 12px; background: white; display: flex; justify-content: space-between; align-items: center;">
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
        '''
    
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
    color_hex = "#ba1a1a" if row['health_status'] == 'Critical' else "#ba6a1a"
    bg_hex = "#ffdad6" if row['health_status'] == 'Critical' else "#ffefd6"
    text_hex = "#ba1a1a" if row['health_status'] == 'Critical' else "#ba6a1a"
    border_hex = "#ffb4ab" if row['health_status'] == 'Critical' else "#ffdfab"
    action = "Intervene" if row['health_status'] == 'Critical' else "Review"
    btn_class = "btn-primary" if row['health_status'] == 'Critical' else "btn-secondary"
    last_active_str = pd.to_datetime(row['last_activity']).strftime('%b %d, %Y') if pd.notna(row['last_activity']) else "No Activity"
    
    account_rows += f"""
        <tr>
            <td><span style="color: {color_hex}; font-size: 10px;">●</span> <strong>{row['company_name']}</strong></td>
            <td><span style="color: {text_hex}; font-weight: 700; font-size: 16px;">{int(row['risk_score'])}</span></td>
            <td>${row['arr']/1000:,.0f}K</td>
            <td style="color: #45464d;">{last_active_str}</td>
            <td><button class="{btn_class}">{action}</button></td>
        </tr>
    """

st.markdown(f"""
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
        {{account_rows}}
    </tbody>
</table>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
