import os
import sqlite3
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_critical_alerts():
    """Query the database for active critical alerts."""
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'churnguard.db'))
    cursor = conn.cursor()
    
    # Get critical customers
    cursor.execute('''
        SELECT company_name, arr, risk_score, health_status, sentiment 
        FROM customers 
        WHERE health_status = 'Critical' OR risk_score >= 80
        ORDER BY arr DESC
    ''')
    
    alerts = cursor.fetchall()
    conn.close()
    return alerts

def format_email_body(alerts):
    """Format alerts into an HTML email body."""
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #dc2626;">🚨 Daily Risk Command Center Report</h2>
        <p>The following accounts require immediate attention. These are flagged as <b>Critical</b> or have a Risk Score of 80+.</p>
        <table style="width: 100%; border-collapse: collapse;">
          <tr style="background-color: #f8fafc; border-bottom: 2px solid #e2e8f0; text-align: left;">
            <th style="padding: 10px;">Company Name</th>
            <th style="padding: 10px;">ARR</th>
            <th style="padding: 10px;">Risk Score</th>
            <th style="padding: 10px;">Sentiment</th>
          </tr>
    """
    
    for company, arr, risk, health, sentiment in alerts:
        # Style formatting based on values
        risk_color = "#dc2626" if risk >= 80 else "#ea580c"
        sentiment_badge = f'<span style="color: #dc2626; font-weight:bold;">{sentiment}</span>' if sentiment == 'Negative' else sentiment
        
        html += f"""
          <tr style="border-bottom: 1px solid #e2e8f0;">
            <td style="padding: 10px; font-weight: bold;">{company}</td>
            <td style="padding: 10px;">${arr/1000:,.0f}k</td>
            <td style="padding: 10px; color: {risk_color}; font-weight: bold;">{risk}</td>
            <td style="padding: 10px;">{sentiment_badge}</td>
          </tr>
        """
        
    html += """
        </table>
        <p style="margin-top: 20px;">Please login to the <a href="#">ChurnGuard Dashboard</a> to review these accounts and initiate intervention playbooks.</p>
        <p style="font-size: 12px; color: #737373;">Automated report generated at {time}</p>
      </body>
    </html>
    """
    return html.replace("{time}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def send_email_report():
    """Send the HTML email report."""
    sender_email = os.environ.get("ALERT_SENDER_EMAIL")
    sender_password = os.environ.get("ALERT_SENDER_PASSWORD")
    recipient_email = os.environ.get("ALERT_RECIPIENT_EMAIL")
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 465))
    
    if not all([sender_email, sender_password, recipient_email]):
        logger.warning("Email credentials missing in .env. Falling back to console logging.")
        alerts = get_critical_alerts()
        if not alerts:
            logger.info("No critical alerts found. Printing nothing.")
            return
        
        # Log to console instead of sending email (for dry runs)
        logger.info("--- START EMAIL DRY RUN ---")
        print(format_email_body(alerts))
        logger.info("--- END EMAIL DRY RUN ---")
        return

    alerts = get_critical_alerts()
    if not alerts:
        logger.info("No critical alerts today. No email sent.")
        return
        
    msg = EmailMessage()
    msg['Subject'] = f'🚨 ChurnGuard: {len(alerts)} Critical Accounts Alert'
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content("Please view this email in an HTML-compatible client.")
    msg.add_alternative(format_email_body(alerts), subtype='html')

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
        logger.info(f"Successfully sent risk alert email to {recipient_email}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_email_report()
