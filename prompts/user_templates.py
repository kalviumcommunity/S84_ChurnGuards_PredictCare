CHURN_PREDICTION_TEMPLATE = """
Please analyze the churn risk for Customer {customer_name} (ID: {customer_id}).

Current Data:
- Risk Score: {risk_score}/100
- Health Status: {health_status}
- Open Tickets: {open_tickets} (Critical: {critical_tickets})
- Days Since Last Activity: {days_since_activity}
- Sentiment: {sentiment}

Based on this information:
1. What are the primary factors driving their current risk score?
2. What immediate actions should the CSM take?
"""

TICKET_SUMMARY_TEMPLATE = """
Please summarize the following support ticket thread for {customer_name}:

Ticket Subject: {ticket_subject}
Priority: {priority}
Created: {created_at}

Thread:
{ticket_thread}

Provide a brief summary of the issue and the current status.
"""
