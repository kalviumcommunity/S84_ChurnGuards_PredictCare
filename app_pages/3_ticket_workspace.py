import streamlit as st
import pandas as pd
from utils.data_loader import inject_custom_css, load_data

_, tickets_df, _, _ = load_data()
inject_custom_css()

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<h2 style="margin-bottom: 4px;">Ticket Workspace</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #45464d;">Manage support queues and active escalations.</p>', unsafe_allow_html=True)
with col2:
    st.markdown('<br>', unsafe_allow_html=True)
    st.text_input("🔍 Search tickets, accounts, or keywords...", label_visibility="collapsed", 
                 placeholder="Search tickets...")

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
    tkt_description = ticket.get('description', ticket.get('subject', 'No details provided.'))
else:
    tkt_id = "TKT-2842"
    tkt_subject = "Data export failing on Q3 Reports Dashboard"
    tkt_customer = "Acme Corp"
    tkt_priority = "Critical"
    tkt_created = "14:23 PM Today"
    tkt_description = "I'm trying to export the Q3 retention reports for our executive review tomorrow, but every time I click the CSV download button, the system hangs and then gives a 504 Gateway Timeout error."
    
priority_badge_class = "badge-critical" if tkt_priority in ['Critical', 'High'] else "badge-medium"
    
# Ticket Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"""
    <div style="margin-bottom: 16px;">
        <span style="background: #e4e2e4; color: #45464d; padding: 2px 8px; border-radius: 4px; font-weight: 500; font-size: 12px; margin-right: 8px;">{tkt_id}</span>
        <span class="badge" style="background: #ffdad6; color: #ba1a1a; border: 1px solid #ffb4ab; padding: 2px 8px;">
            <span class="material-symbols-outlined" style="font-size: 14px; vertical-align: text-bottom;">timer</span> SLA: 2h 14m
        </span>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div style="display: flex; gap: 8px; justify-content: flex-end;">
            <a href="#" class="btn-secondary" style="padding: 6px 12px; font-size: 13px;"><span class="material-symbols-outlined" style="font-size: 16px;">person_add</span> Assign</a>
            <a href="#" class="btn-primary" style="padding: 6px 12px; font-size: 13px;">Resolve</a>
        </div>
    """, unsafe_allow_html=True)

# Ticket Title
st.markdown(f'<h1 style="font-size: 24px !important; margin-bottom: 8px !important;">{tkt_subject}</h1>', unsafe_allow_html=True)
st.markdown(f"""
<div style="display: flex; gap: 16px; color: #45464d; font-size: 14px; margin-bottom: 16px;">
    <div style="display: flex; align-items: center; gap: 4px;">
        <span class="material-symbols-outlined" style="font-size: 16px;">account_circle</span> Sarah Jenkins ({tkt_customer})
    </div>
    <div style="display: flex; align-items: center; gap: 4px;">
        <span class="material-symbols-outlined" style="font-size: 16px;">schedule</span> Created: {tkt_created}
    </div>
    <div style="display: flex; align-items: center; gap: 4px;">
        <span class="material-symbols-outlined" style="font-size: 16px;">flag</span> Priority: {tkt_priority}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Conversation Thread
col1, col2 = st.columns([4, 1])

with col1:
    # Customer Message
    st.markdown(f"""
    <div style="background: #ffffff; border: 1px solid #c6c6cd; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
        <div style="display: flex; gap: 12px;">
            <div style="width: 36px; height: 36px; background: #d3e4fe; border-radius: 50%; 
                       display: flex; align-items: center; justify-content: center; color: #0b1c30; 
                       font-weight: 600; flex-shrink: 0;">SJ</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; margin-bottom: 8px; color: #1b1b1d;">Sarah Jenkins ({tkt_customer})</div>
                <div style="color: #45464d; line-height: 1.6; font-size: 14px;">
                    {tkt_description}
                </div>
                <div style="text-align: right; color: #76777d; font-size: 12px; margin-top: 8px;">{tkt_created}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # System Note
    st.markdown("""
    <div style="background: #f0edef; padding: 16px; border-radius: 8px; border-left: 4px solid #45464d; margin-bottom: 16px;">
        <div style="display: flex; gap: 12px; align-items: start;">
            <span class="material-symbols-outlined" style="color: #45464d;">smart_toy</span>
            <div>
                <div style="font-weight: 600; margin-bottom: 4px; color: #1b1b1d; font-size: 14px;">Internal Note (System)</div>
                <div style="color: #45464d; font-size: 13px;">
                    <strong>Automated Risk Analysis:</strong> Customer sentiment is highly negative. 
                    Account is in Renewal Phase (30 days remaining). Export functionality is a known issue 
                    for large datasets on legacy infrastructure (Ticket #ENG-491).
                </div>
                <div style="text-align: right; color: #76777d; font-size: 12px; margin-top: 8px;">14:23 PM</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Agent Response Box
    st.markdown("""
    <div style="background: white; border: 1px solid #c6c6cd; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
        <div style="display: flex; gap: 12px; margin-bottom: 12px;">
            <div style="width: 36px; height: 36px; background: #000000; border-radius: 50%; 
                       display: flex; align-items: center; justify-content: center; color: white; 
                       font-weight: 600; flex-shrink: 0;">You</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; margin-bottom: 4px;">You (Agent)</div>
                <div style="color: #76777d; font-size: 12px;">14:45 PM</div>
            </div>
        </div>
        <div style="color: #45464d; line-height: 1.6; margin-bottom: 16px; font-size: 14px;">
            Hi Sarah,<br><br>
            I completely understand the urgency for your board meeting. I'm looking into this 
            immediately. Our engineering team is currently investigating a known timeout issue with 
            exceptionally large data exports.
        </div>
    </div>
    
    <div style="margin-top: 16px;">
        <input type="text" placeholder="Type your reply or add an internal note..." 
               style="width: 100%; padding: 12px; border: 1px solid #c6c6cd; border-radius: 6px; 
                      font-size: 14px; font-family: Inter;">
    </div>
    
    <div style="margin-top: 12px; display: flex; justify-content: space-between; align-items: center;">
        <label style="font-size: 13px; color: #45464d;">
            <input type="checkbox"> Internal Note
        </label>
        <div style="display: flex; gap: 8px;">
            <a href="#" class="btn-secondary">Save Draft</a>
            <a href="#" class="btn-primary">Send <span class="material-symbols-outlined" style="font-size: 16px; margin-left: 4px;">send</span></a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Customer 360 Context Panel
    st.markdown('<div class="content-card" style="position: sticky; top: 20px;">', unsafe_allow_html=True)
    st.markdown("### Customer 360 Context")
    
    st.markdown("""
    <div style="text-align: center; padding: 16px 0; border-bottom: 1px solid #e4e2e4;">
        <div style="width: 48px; height: 48px; background: #f0edef; border-radius: 50%; 
                   display: flex; align-items: center; justify-content: center; margin: 0 auto 8px; 
                   font-weight: 700; font-size: 18px; color: #1b1b1d;">AC</div>
        <div style="font-weight: 600; color: #1b1b1d;">Acme Corp</div>
        <div style="font-size: 12px; color: #45464d;">Enterprise Tier • Tech</div>
    </div>
    
    <div style="padding: 16px 0; border-bottom: 1px solid #e4e2e4;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 16px;">
            <div style="text-align: center;">
                <div style="font-size: 11px; color: #45464d; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">Risk Score</div>
                <div style="font-size: 28px; font-weight: 700; color: #ba1a1a;">72<span style="font-size: 16px; color: #76777d;">/100</span></div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 11px; color: #45464d; text-transform: uppercase; margin-bottom: 4px; font-weight: 600;">ARR</div>
                <div style="font-size: 28px; font-weight: 700; color: #000000;">$145k</div>
            </div>
        </div>
        <div style="margin-bottom: 12px;">
            <div style="font-size: 11px; color: #45464d; margin-bottom: 4px; font-weight: 600;">Sentiment</div>
            <span class="badge badge-critical">😟 Negative</span>
        </div>
        <div>
            <div style="font-size: 11px; color: #45464d; margin-bottom: 4px; font-weight: 600;">Renewal Date</div>
            <div style="font-size: 14px; color: #1b1b1d;">Oct 15 (28 days)</div>
        </div>
    </div>
    
    <div style="padding: 16px 0; background: #ffdad6; margin: 0 -24px; padding: 16px 24px; color: #ba1a1a; border-bottom: 1px solid #ffb4ab;">
        <div style="font-weight: 600; margin-bottom: 8px; display: flex; align-items: center; gap: 4px;">
            <span class="material-symbols-outlined" style="font-size: 18px;">warning</span> Active Escalation
        </div>
        <div style="font-size: 13px; font-weight: 500;">
            Level 2 - Executive Review Required. Flagged due to repeated core feature failure.
        </div>
    </div>
    
    <div style="padding: 16px 0; background: #d3e4fe; margin: 0 -24px; padding: 16px 24px;">
        <div style="font-weight: 600; margin-bottom: 8px; color: #0b1c30; display: flex; align-items: center; gap: 4px;">
            <span class="material-symbols-outlined" style="font-size: 18px;">lightbulb</span> AI RECOMMENDATION
        </div>
        <div style="font-size: 13px; color: #0b1c30;">
            Offer a 1-on-1 strategy call with a Success Manager to address feature friction 
            and bypass standard queue.
        </div>
        <div style="margin-top: 12px;">
            <a href="#" class="btn-primary" style="width: 100%; text-align: center;">
                Draft Invitation
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h3 style="font-size: 16px !important;">Recent Interactions</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #e4e2e4;">
        <div style="display: flex; gap: 8px;">
            <span class="material-symbols-outlined" style="color: #76777d;">edit_note</span>
            <div style="flex: 1;">
                <div style="font-weight: 500; font-size: 13px; color: #1b1b1d;">NPS Survey Submitted</div>
                <div style="font-size: 12px; color: #45464d;">Score: 4/10 (Detractor)</div>
                <div style="font-size: 11px; color: #76777d; margin-top: 4px;">2 days ago</div>
            </div>
        </div>
    </div>
    
    <div style="margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #e4e2e4;">
        <div style="display: flex; gap: 8px;">
            <span class="material-symbols-outlined" style="color: #166534;">check_circle</span>
            <div style="flex: 1;">
                <div style="font-weight: 500; font-size: 13px; color: #1b1b1d;">Ticket Resolved</div>
                <div style="font-size: 12px; color: #45464d;">Dashboard UI Glitch</div>
                <div style="font-size: 11px; color: #76777d; margin-top: 4px;">5 days ago</div>
            </div>
        </div>
    </div>
    
    <div style="margin-bottom: 16px;">
        <div style="display: flex; gap: 8px;">
            <span class="material-symbols-outlined" style="color: #76777d;">event</span>
            <div style="flex: 1;">
                <div style="font-weight: 500; font-size: 13px; color: #1b1b1d;">QBR Completed</div>
                <div style="font-size: 12px; color: #45464d;">Attended by VP Eng</div>
                <div style="font-size: 11px; color: #76777d; margin-top: 4px;">3 weeks ago</div>
            </div>
        </div>
    </div>
    
    <a href="#" style="font-size: 13px; color: #000000; text-decoration: underline; font-weight: 500;">
        View Full History
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
