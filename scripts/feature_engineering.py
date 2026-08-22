import pandas as pd
import numpy as np

def engineer_features(customers, tickets, interactions):
    """
    Engineers features like risk_score based on tickets and interactions.
    """
    if customers.empty:
        # Create sample customers if empty
        customers = pd.DataFrame({
            'customer_id': range(1, 201),
            'company_name': [f'Company {chr(65 + i % 26)}{i}' for i in range(1, 201)],
            'arr': np.random.randint(50000, 5000000, 200),
            'sentiment': np.random.choice(['Positive', 'Neutral', 'Negative'], 200, p=[0.3, 0.4, 0.3])
        })
        
    # Ensure arr column exists
    if 'arr' not in customers.columns:
        customers['arr'] = np.random.randint(50000, 5000000, len(customers))
    
    # Ensure sentiment column exists
    if 'sentiment' not in customers.columns:
        customers['sentiment'] = np.random.choice(['Positive', 'Neutral', 'Negative'], len(customers), p=[0.3, 0.4, 0.3])
        
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
    else:
        # Add default last_activity if no interactions
        customers['last_activity'] = pd.to_datetime('today') - pd.to_timedelta(np.random.randint(1, 30, len(customers)), unit='d')
        customers['days_since_active'] = np.random.randint(1, 30, len(customers))
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
        
    # Calculate mathematical churn probability
    inactivity = customers.get('days_since_active', 0)
    neg_tix = customers.get('negative_tickets', 0)
    crit_tix = customers.get('critical_tickets', 0)
    
    # Base churn risk = 5% (0.05)
    # Usage drops = 0.5% (0.005) per day of inactivity
    # Ticket sentiment = 10% (0.10) per negative ticket
    # Critical issues = 15% (0.15) per critical ticket
    churn_prob = 0.05 + (inactivity * 0.005) + (neg_tix * 0.10) + (crit_tix * 0.15)
    
    # Cap between 1% and 99%
    customers['predicted_churn_prob'] = churn_prob.clip(lower=0.01, upper=0.99)
    
    # Round to 4 decimal places for precision
    customers['predicted_churn_prob'] = customers['predicted_churn_prob'].round(4)
        
    return customers, tickets
