import pandas as pd
import numpy as np
from datetime import datetime

def engineer_features(customers, tickets, interactions):
    """
    Engineers features like risk_score based on tickets and interactions.
    """
    if customers.empty:
        return customers, tickets
        
    # Base risk score calculation
    customers['risk_score'] = 20 # Base risk
    
    # 1. High priority unresolved tickets
    if not tickets.empty:
        unresolved = tickets[tickets['status'] != 'Resolved']
        critical_tickets = unresolved[unresolved['priority'] == 'Critical'].groupby('customer_id').size()
        high_tickets = unresolved[unresolved['priority'] == 'High'].groupby('customer_id').size()
        
        customers = customers.merge(critical_tickets.rename('critical_tickets'), on='customer_id', how='left')
        customers = customers.merge(high_tickets.rename('high_tickets'), on='customer_id', how='left')
        
        customers['critical_tickets'] = customers['critical_tickets'].fillna(0)
        customers['high_tickets'] = customers['high_tickets'].fillna(0)
        
        customers['risk_score'] += (customers['critical_tickets'] * 15) + (customers['high_tickets'] * 10)
        
        # Negative sentiment in tickets
        negative_tickets = tickets[tickets['sentiment'] == 'Negative'].groupby('customer_id').size()
        customers = customers.merge(negative_tickets.rename('negative_tickets'), on='customer_id', how='left')
        customers['negative_tickets'] = customers['negative_tickets'].fillna(0)
        customers['risk_score'] += (customers['negative_tickets'] * 5)
        
    # 2. Add last activity
    if not interactions.empty:
        last_activity = interactions.groupby('customer_id')['timestamp'].max()
        customers = customers.merge(last_activity.rename('last_activity'), on='customer_id', how='left')
        
        # Calculate days since last activity
        now = pd.to_datetime('today')
        customers['days_since_active'] = (now - customers['last_activity']).dt.days
        customers['days_since_active'] = customers['days_since_active'].fillna(30)
        
        # Add risk based on inactivity
        customers['risk_score'] += np.where(customers['days_since_active'] > 30, 20, 0)
        
    # Ensure risk score is capped at 100
    customers['risk_score'] = customers['risk_score'].clip(upper=100)
    
    # Determine health status based on risk score
    def get_health_status(score):
        if score >= 75:
            return 'Critical'
        elif score >= 50:
            return 'Medium'
        else:
            return 'Low Risk'
            
    customers['health_status'] = customers['risk_score'].apply(get_health_status)
    
    # Add dummy risk score to tickets for existing UI
    if not tickets.empty:
        tickets = tickets.merge(customers[['customer_id', 'risk_score', 'company_name']], on='customer_id', how='left')
        tickets = tickets.rename(columns={'company_name': 'company'})
        # Use first name from customer_id as dummy customer name
        tickets['customer'] = 'User ' + tickets['customer_id'].str.split('-').str[1]
        
    return customers, tickets
