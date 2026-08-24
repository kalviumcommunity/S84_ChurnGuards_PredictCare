import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.data_loader import inject_custom_css, load_data, export_customer_data

customers_df, tickets_df, interactions_df, _ = load_data()
inject_custom_css()

# --- NEW FILTERS SECTION ---
st.markdown("### 🔍 Search & Filter")
    
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    search_term = st.text_input("Search by Company Name", "")
    
with filter_col2:
    if not customers_df.empty and 'industry' in customers_df.columns:
        industries = ["All"] + sorted(customers_df['industry'].dropna().unique().tolist())
    else:
        industries = ["All", "Technology", "Financial Technology"]
    selected_industry = st.selectbox("Industry", industries)
    
with filter_col3:
    health_statuses = ["All", "Critical", "Medium", "Low Risk"]
    selected_health = st.multiselect("Health Status", health_statuses, default=["All"])
    
arr_range = st.slider("Min ARR ($)", 
                      min_value=0, 
                      max_value=int(customers_df['arr'].max()) if not customers_df.empty and 'arr' in customers_df.columns else 1000000, 
                      value=0, 
                      step=10000)

st.markdown("<hr>", unsafe_allow_html=True)

# Apply filters
filtered_df = customers_df.copy()
if not filtered_df.empty:
    if search_term:
        filtered_df = filtered_df[filtered_df['company_name'].str.contains(search_term, case=False, na=False)]
    if selected_industry != "All":
        filtered_df = filtered_df[filtered_df['industry'] == selected_industry]
    if "All" not in selected_health and selected_health:
        filtered_df = filtered_df[filtered_df['health_status'].isin(selected_health)]
    filtered_df = filtered_df[filtered_df['arr'] >= arr_range]

# Dynamic Customer Profile Selection
if not filtered_df.empty:
    st.markdown(f"**Found {len(filtered_df)} matching customers.**")
    company_names = filtered_df['company_name'].tolist()
    
    # Determine index for selectbox (default to a critical customer if available)
    default_idx = 0
    criticals = filtered_df[filtered_df['health_status'] == 'Critical']
    if not criticals.empty:
        critical_company = criticals.sort_values('risk_score', ascending=False).iloc[0]['company_name']
        default_idx = company_names.index(critical_company)
        
    selected_company = st.selectbox("Select a Customer to View Profile", company_names, index=default_idx)
    cust = filtered_df[filtered_df['company_name'] == selected_company].iloc[0]
        
    cust_name = cust['company_name']
    cust_id = cust.get('customer_id')
    cust_risk = int(cust['risk_score'])
    cust_arr = cust['arr']
    cust_renewal = pd.to_datetime(cust['renewal_date']).strftime('%b %d') if pd.notna(cust['renewal_date']) else "Unknown"
    cust_industry = cust.get('industry', 'Technology')
    cust_size = cust.get('company_size', 'Enterprise')
    
    # Filter tickets for this customer (PR 16)
    if not tickets_df.empty and cust_id is not None:
        matching_tickets = tickets_df[
            (tickets_df['customer_id'] == cust_id) | 
            (tickets_df['customer_id'] == f"CUST-{cust_id}") |
            (tickets_df['customer_id'].astype(str) == str(cust_id))
        ].copy()
        if matching_tickets.empty and 'company' in tickets_df.columns:
            matching_tickets = tickets_df[tickets_df['company'] == cust_name].copy()
    else:
        matching_tickets = pd.DataFrame()
        
    sort_col = 'created_at' if 'created_at' in matching_tickets.columns else ('created_date' if 'created_date' in matching_tickets.columns else None)
    if sort_col and not matching_tickets.empty:
        matching_tickets[sort_col] = pd.to_datetime(matching_tickets[sort_col], errors='coerce')
        recent_tickets = matching_tickets.sort_values(sort_col, ascending=False).head(5)
    else:
        recent_tickets = matching_tickets.head(5)
    
    # ML outputs
    cust_churn_prob = cust.get('predicted_churn_prob', np.nan)
    cust_clv = cust.get('clv_forecast', np.nan)
else:
    cust_name = "GlobalTech Inc."
    cust_id = 1
    cust_risk = 88
    cust_arr = 1200000
    cust_renewal = "Oct 15"
    cust_industry = "Financial Technology"
    cust_size = "5,000+ Employees"
    cust_churn_prob = 0.85
    cust_clv = 1500000
    matching_tickets = pd.DataFrame()
    recent_tickets = pd.DataFrame()

arr_display = f"${cust_arr/1000000:.1f}M" if cust_arr >= 1000000 else f"${cust_arr/1000:,.0f}K"

# ML Formatting
prob_display = f"{cust_churn_prob*100:.1f}%" if pd.notna(cust_churn_prob) else "N/A"
clv_display = f"${cust_clv/1000000:.1f}M" if pd.notna(cust_clv) and cust_clv >= 1000000 else (f"${cust_clv/1000:,.0f}K" if pd.notna(cust_clv) else "N/A")
risk_badge = f'<span class="badge" style="background: #dc2626; color: white; font-size: 14px;">⚠️ Churn Risk: High ({cust_risk})</span>' if cust_risk >= 75 else f'<span class="badge" style="background: #f59e0b; color: white; font-size: 14px;">Medium Risk ({cust_risk})</span>'

# Header Box mimicking Stitch Customer 360 Header
st.markdown(f"""
<div class="content-card" style="display: flex; justify-content: space-between; align-items: center; padding: 24px;">
    <div style="display: flex; align-items: center; gap: 24px;">
        <div style="width: 64px; height: 64px; background: #f0edef; border-radius: 8px; border: 1px solid #c6c6cd; 
                   display: flex; align-items: center; justify-content: center; font-size: 24px; color: #1b1b1d; font-weight: 700;">
            {cust_name[:2].upper()}
        </div>
        <div>
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <h2 style="margin: 0 !important; font-size: 32px !important; color: #1b1b1d !important;">{cust_name}</h2>
                <span class="badge" style="background: {'#ffdad6' if cust_risk >= 75 else '#ffefd6'}; 
                                         color: {'#ba1a1a' if cust_risk >= 75 else '#ba6a1a'}; 
                                         border: 1px solid {'#ffb4ab' if cust_risk >= 75 else '#ffdfab'}; 
                                         display: inline-flex; align-items: center; gap: 4px;">
                    <span class="material-symbols-outlined" style="font-size: 16px;">warning</span> 
                    Churn Risk: {'High' if cust_risk >= 75 else 'Medium'} ({cust_risk})
                </span>
            </div>
            <div style="display: flex; gap: 24px; color: #45464d; font-size: 14px;">
                <span style="display: flex; align-items: center; gap: 4px;"><span class="material-symbols-outlined" style="font-size: 16px;">public</span> {cust_industry}</span>
                <span style="display: flex; align-items: center; gap: 4px;"><span class="material-symbols-outlined" style="font-size: 16px;">account_balance_wallet</span> ARR: {arr_display}</span>
                <span style="display: flex; align-items: center; gap: 4px;"><span class="material-symbols-outlined" style="font-size: 16px;">calendar_today</span> Renewal: {cust_renewal}</span>
            </div>
        </div>
    </div>
    <div style="display: flex; gap: 12px;">
        <a href="#" class="btn-primary" style="display: inline-flex; align-items: center; gap: 4px;">
            <span class="material-symbols-outlined" style="font-size: 18px;">bolt</span> Initiate Intervention
        </a>
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
        <div style="font-size: 11px; color: #45464d; text-transform: uppercase; font-weight: 600; margin-bottom: 4px; letter-spacing: 0.5px;">INDUSTRY</div>
        <div style="color: #1b1b1d; font-size: 14px;">{cust_industry}</div>
    </div>
    
    <div style="margin-bottom: 16px;">
        <div style="font-size: 11px; color: #45464d; text-transform: uppercase; font-weight: 600; margin-bottom: 4px; letter-spacing: 0.5px;">COMPANY SIZE</div>
        <div style="color: #1b1b1d; font-size: 14px;">{cust_size if pd.notna(cust_size) else "Unknown"}</div>
    </div>
    
    <div style="margin-bottom: 16px;">
        <div style="font-size: 11px; color: #45464d; text-transform: uppercase; font-weight: 600; margin-bottom: 4px; letter-spacing: 0.5px;">TENURE</div>
        <div style="color: #1b1b1d; font-size: 14px;">3 Years, 4 Months</div>
    </div>
    
    <div style="margin-bottom: 16px;">
        <div style="font-size: 11px; color: #45464d; text-transform: uppercase; font-weight: 600; margin-bottom: 4px; letter-spacing: 0.5px;">KEY STAKEHOLDER</div>
        <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
            <div style="width: 24px; height: 24px; border-radius: 50%; background: #d3e4fe; display: flex; align-items: center; justify-content: center; color: #0b1c30; font-size: 10px; font-weight: 600; flex-shrink: 0;">EJ</div>
            <span style="color: #1b1b1d; font-size: 14px;">Elena Jenkins, VP Ops</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Health Metrics
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Health Metrics")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div style="text-align: left; background: #f6f3f5; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
            <div style="font-size: 12px; color: #45464d; margin-bottom: 4px; font-weight: 500; font-family: monospace;">ML Churn Probability</div>
            <div style="display: flex; align-items: baseline; gap: 8px;">
                <div style="font-size: 24px; font-weight: 700; color: #1b1b1d;">{prob_display}</div>
                <div style="font-size: 12px; color: #ba1a1a; display: flex; align-items: center;"><span class="material-symbols-outlined" style="font-size: 14px;">trending_down</span> Based on ML</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div style="text-align: left; background: #f6f3f5; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
            <div style="font-size: 12px; color: #45464d; margin-bottom: 4px; font-weight: 500; font-family: monospace;">Usage (WAU)</div>
            <div style="display: flex; align-items: baseline; gap: 8px;">
                <div style="font-size: 24px; font-weight: 700; color: #1b1b1d;">1,240</div>
                <div style="font-size: 12px; color: #ba1a1a; display: flex; align-items: center;"><span class="material-symbols-outlined" style="font-size: 14px;">trending_down</span> 15%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    open_cust_tix = len(matching_tickets[matching_tickets['status'].isin(['Open', 'In Progress'])]) if not matching_tickets.empty and 'status' in matching_tickets.columns else 0
    crit_cust_tix = len(matching_tickets[(matching_tickets['priority'] == 'Critical') & (matching_tickets['status'].isin(['Open', 'In Progress']))]) if not matching_tickets.empty and 'priority' in matching_tickets.columns and 'status' in matching_tickets.columns else 0
    
    st.markdown(f"""
    <div style="text-align: left; background: #f6f3f5; padding: 12px; border-radius: 8px; margin-top: 8px;">
        <div style="font-size: 12px; color: #45464d; margin-bottom: 4px; font-weight: 500; font-family: monospace;">Open Support Tickets</div>
        <div style="display: flex; align-items: baseline; gap: 8px;">
            <div style="font-size: 24px; font-weight: 700; color: #1b1b1d;">{open_cust_tix}</div>
            <div style="font-size: 12px; color: {'#ba1a1a' if open_cust_tix > 0 else '#166534'}; display: flex; align-items: center;"><span class="material-symbols-outlined" style="font-size: 14px;">trending_up</span> {crit_cust_tix} Critical</div>
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
    
    st.html("""
    <div style="margin-top: 20px; position: relative;">
        <!-- Timeline Line -->
        <div style="position: absolute; left: 15px; top: 0; bottom: 0; width: 2px; background: #c6c6cd; z-index: 0;"></div>
        
        <div style="display: flex; gap: 12px; margin-bottom: 20px; position: relative; z-index: 10;">
            <div style="width: 32px; height: 32px; background: #ffdad6; border-radius: 50%; border: 2px solid #ffffff;
                       display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <span class="material-symbols-outlined" style="color: #ba1a1a; font-size: 16px;">mood_bad</span>
            </div>
            <div style="flex: 1; background: #f6f3f5; border: 1px solid #ffdad6; padding: 12px; border-radius: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <div style="font-weight: 700; color: #1b1b1d; font-size: 13px;">Negative Sentiment Detected</div>
                    <div style="font-size: 12px; color: #45464d;">Today, 10:14 AM</div>
                </div>
                <div style="font-size: 13px; color: #45464d;">
                    AI detected high frustration in recent email thread regarding API downtime.
                </div>
            </div>
        </div>
        
        <div style="display: flex; gap: 12px; margin-bottom: 20px; position: relative; z-index: 10;">
            <div style="width: 32px; height: 32px; background: #f0edef; border-radius: 50%; border: 2px solid #ffffff;
                       display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <span class="material-symbols-outlined" style="color: #1b1b1d; font-size: 16px;">confirmation_number</span>
            </div>
            <div style="flex: 1; background: #f6f3f5; border: 1px solid #c6c6cd; padding: 12px; border-radius: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <div style="font-weight: 700; color: #1b1b1d; font-size: 13px;">Ticket #8842 Escalated</div>
                    <div style="font-size: 12px; color: #45464d;">Yesterday, 3:45 PM</div>
                </div>
                <div style="font-size: 13px; color: #45464d;">
                    Subject: "Data Sync Failure" - Clicked to Tier 3 Support. Assigned.
                </div>
            </div>
        </div>
        
        <div style="display: flex; gap: 12px; margin-bottom: 20px; position: relative; z-index: 10;">
            <div style="width: 32px; height: 32px; background: #ffefd6; border-radius: 50%; border: 2px solid #ffffff;
                       display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <span class="material-symbols-outlined" style="color: #ba6a1a; font-size: 16px;">trending_down</span>
            </div>
            <div style="flex: 1; background: #f6f3f5; border: 1px solid #ffdfab; padding: 12px; border-radius: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <div style="font-weight: 700; color: #1b1b1d; font-size: 13px;">Significant Usage Drop</div>
                    <div style="font-size: 12px; color: #45464d;">Oct 2, 2023</div>
                </div>
                <div style="font-size: 13px; color: #45464d;">
                    Active users dropped by 22% compared to previous 30-day moving average.
                </div>
            </div>
        </div>
        
        <div style="display: flex; gap: 12px; margin-bottom: 20px; position: relative; z-index: 10;">
            <div style="width: 32px; height: 32px; background: #f0edef; border-radius: 50%; border: 2px solid #ffffff;
                       display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <span class="material-symbols-outlined" style="color: #1b1b1d; font-size: 16px;">call</span>
            </div>
            <div style="flex: 1; background: #f6f3f5; border: 1px solid #c6c6cd; padding: 12px; border-radius: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <div style="font-weight: 700; color: #1b1b1d; font-size: 13px;">Q3 Review Call</div>
                    <div style="font-size: 12px; color: #45464d;">Sep 15, 2023</div>
                </div>
                <div style="font-size: 13px; color: #45464d;">
                    Standard check-in. Client noted concerns about feature roadmap pacing.
                </div>
            </div>
        </div>
    </div>
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # Retention Strategy
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Retention Strategy")
    
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div style="font-size: 11px; color: #45464d; text-transform: uppercase; font-weight: 600; margin-bottom: 8px; letter-spacing: 0.5px;">
            PRIMARY RISK FACTORS
        </div>
        <ul style="padding-left: 20px; margin: 0; color: #1b1b1d; font-size: 14px; line-height: 1.6;">
            <li style="margin-bottom: 6px;">Recurring API instability (#8682)</li>
            <li style="margin-bottom: 6px;">Poor sentiment in recent communication</li>
            <li style="margin-bottom: 6px;">Low adoption of new Reporting Module</li>
        </ul>
    </div>
    
    <div style="margin-bottom: 20px;">
        <div style="font-size: 11px; color: #45464d; text-transform: uppercase; font-weight: 600; margin-bottom: 8px; letter-spacing: 0.5px;">
            RECOMMENDED ACTIONS
        </div>
        <div style="margin-bottom: 12px; background: #f6f3f5; padding: 12px; border-radius: 8px;">
            <div style="display: flex; align-items: start; gap: 8px;">
                <input type="checkbox" id="action1" style="margin-top: 4px;">
                <div>
                    <label for="action1" style="font-size: 13px; color: #1b1b1d; font-weight: 600;">Schedule Executive Sync</label>
                    <div style="font-size: 12px; color: #45464d; margin-top: 4px;">
                        Engage Elena Jenkins immediately to discuss API stability roadmap.
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-bottom: 12px; background: #f6f3f5; padding: 12px; border-radius: 8px;">
            <div style="display: flex; align-items: start; gap: 8px;">
                <input type="checkbox" id="action2" style="margin-top: 4px;">
                <div>
                    <label for="action2" style="font-size: 13px; color: #1b1b1d; font-weight: 600;">Offer Tech Deep-Dive</label>
                    <div style="font-size: 12px; color: #45464d; margin-top: 4px;">
                        Propose 1-on-1 session with Solutions Architect to optimize API usage.
                    </div>
                </div>
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
    <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: #f6f3f5; 
               border-radius: 8px; margin-bottom: 12px;">
        <div style="width: 36px; height: 36px; background: #d3e4fe; border-radius: 50%; 
                   display: flex; align-items: center; justify-content: center; font-weight: 600; 
                   color: #0b1c30; flex-shrink: 0; font-size: 12px;">SM</div>
        <div style="flex: 1;">
            <div style="font-weight: 600; font-size: 13px; color: #1b1b1d;">Sarah Miller</div>
            <div style="font-size: 12px; color: #45464d;">Customer Success Mgr</div>
        </div>
        <span class="material-symbols-outlined" style="color: #45464d; font-size: 18px;">mail</span>
    </div>
    
    <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: #f6f3f5; 
               border-radius: 8px; margin-bottom: 12px;">
        <div style="width: 36px; height: 36px; background: #ffefd6; border-radius: 50%; 
                   display: flex; align-items: center; justify-content: center; font-weight: 600; 
                   color: #ba6a1a; flex-shrink: 0; font-size: 12px;">DR</div>
        <div style="flex: 1;">
            <div style="font-weight: 600; font-size: 13px; color: #1b1b1d;">David Rossi</div>
            <div style="font-size: 12px; color: #45464d;">Account Executive</div>
        </div>
        <span class="material-symbols-outlined" style="color: #45464d; font-size: 18px;">mail</span>
    </div>
    
    <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: #f6f3f5; 
               border-radius: 8px;">
        <div style="width: 36px; height: 36px; background: #DCFCE7; border-radius: 50%; 
                   display: flex; align-items: center; justify-content: center; font-weight: 600; 
                   color: #166534; flex-shrink: 0; font-size: 12px;">KL</div>
        <div style="flex: 1;">
            <div style="font-weight: 600; font-size: 13px; color: #1b1b1d;">Kevin Lee</div>
            <div style="font-size: 12px; color: #45464d;">Tier 3 Support Lead</div>
        </div>
        <span class="material-symbols-outlined" style="color: #45464d; font-size: 18px;">mail</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------
# PR 16: Customer 360 Expansion - 5 Most Recent Support Tickets
# --------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="content-card">', unsafe_allow_html=True)

col_tbl_h1, col_tbl_h2 = st.columns([3, 1])
with col_tbl_h1:
    st.markdown("### 🎫 Recent Support Tickets (Customer 360)")
    st.markdown(f"<span style='font-size: 13px; color: #64748B;'>5 most recent support tickets for <b>{cust_name}</b></span>", unsafe_allow_html=True)
with col_tbl_h2:
    st.markdown(f'<div style="text-align: right;"><span class="badge badge-medium">{len(matching_tickets)} Total Recorded</span></div>', unsafe_allow_html=True)

if not recent_tickets.empty:
    ticket_rows = ""
    for _, tkt in recent_tickets.iterrows():
        prio = str(tkt.get('priority', 'Medium'))
        if prio == "Critical":
            prio_badge = '<span class="badge badge-critical">Critical</span>'
        elif prio == "High":
            prio_badge = '<span class="badge badge-high">High</span>'
        elif prio == "Medium":
            prio_badge = '<span class="badge badge-medium">Medium</span>'
        else:
            prio_badge = '<span class="badge badge-low">Low</span>'
            
        status_val = str(tkt.get('status', 'Open'))
        status_color = "#000000" if status_val in ['Open', 'In Progress'] else ("#166534" if status_val in ['Resolved', 'Closed'] else "#ba6a1a")
        
        sent_val = str(tkt.get('sentiment', 'Neutral'))
        if sent_val == 'Negative':
            sent_badge = '<span class="badge badge-critical">😟 Negative</span>'
        elif sent_val == 'Positive':
            sent_badge = '<span class="badge badge-low">😊 Positive</span>'
        else:
            sent_badge = '<span class="badge badge-medium">😐 Neutral</span>'
            
        date_col = tkt.get('created_at', tkt.get('created_date'))
        date_str = pd.to_datetime(date_col).strftime('%b %d, %Y') if pd.notna(date_col) else "Recent"
        
        tkt_subj = str(tkt.get('subject', 'Support Request'))
        if len(tkt_subj) > 55:
            tkt_subj = tkt_subj[:52] + "..."
            
        tkt_id_display = str(tkt.get('ticket_id', 'TKT-000'))
        
        ticket_rows += f"""
        <tr>
            <td><strong style="color: #000000; font-family: monospace;">{tkt_id_display}</strong></td>
            <td style="color: #1b1b1d;">{tkt_subj}</td>
            <td>{prio_badge}</td>
            <td><span style="color: {status_color}; font-weight: 600;">● {status_val}</span></td>
            <td>{sent_badge}</td>
            <td style="color: #45464d;">{date_str}</td>
            <td><a href="#" class="btn-secondary" style="padding: 4px 10px; font-size: 11px;">View</a></td>
        </tr>
        """
        
    st.markdown(f"""
    <div style="overflow-x: auto;">
        <table class="data-table" style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr>
                    <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e4e2e4; color: #45464d; font-size: 12px;">TICKET ID</th>
                    <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e4e2e4; color: #45464d; font-size: 12px;">SUBJECT</th>
                    <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e4e2e4; color: #45464d; font-size: 12px;">PRIORITY</th>
                    <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e4e2e4; color: #45464d; font-size: 12px;">STATUS</th>
                    <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e4e2e4; color: #45464d; font-size: 12px;">SENTIMENT</th>
                    <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e4e2e4; color: #45464d; font-size: 12px;">CREATED DATE</th>
                    <th style="padding: 12px; text-align: left; border-bottom: 2px solid #e4e2e4; color: #45464d; font-size: 12px;">ACTION</th>
                </tr>
            </thead>
            <tbody>
                {ticket_rows}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 32px 0; color: #64748B;">
        <div style="font-size: 32px; margin-bottom: 8px;">📋</div>
        <div style="font-weight: 600; font-size: 15px; color: #0F172A;">No Support Tickets Found</div>
        <div style="font-size: 13px; margin-top: 4px;">There are currently no support tickets associated with this account.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
