import streamlit as st
import pandas as pd

def render_risk_center(customers_df, get_risk_alert_summary):
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
