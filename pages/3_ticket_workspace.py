import streamlit as st
import pandas as pd
from utils.data_loader import inject_custom_css, load_data

_, tickets_df, _, _ = load_data()
inject_custom_css()

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
