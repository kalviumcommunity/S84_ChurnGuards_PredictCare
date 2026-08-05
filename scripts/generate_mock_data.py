import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

np.random.seed(42)

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# 1. Generate customers.csv
num_customers = 200
customer_ids = [f'CUST-{1000+i}' for i in range(num_customers)]
customers = pd.DataFrame({
    'customer_id': customer_ids,
    'company_name': [f'Company {chr(65 + (i % 26))}{i}' for i in range(num_customers)],
    'industry': np.random.choice(['Tech', 'Retail', 'Finance', 'Healthcare', 'Manufacturing'], num_customers),
    'arr': np.random.randint(50000, 5000000, num_customers),
    'contract_type': np.random.choice(['Monthly', 'Annual', 'Multi-year'], num_customers, p=[0.2, 0.6, 0.2]),
    'renewal_date': [(datetime.now() + timedelta(days=np.random.randint(1, 365))).strftime('%Y-%m-%d') for _ in range(num_customers)],
    'csm_name': np.random.choice(['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'], num_customers)
})
customers.to_csv('data/customers.csv', index=False)

# 2. Generate tickets.json
num_tickets = 500
tickets = []
for i in range(num_tickets):
    created = datetime.now() - timedelta(days=np.random.randint(1, 100), hours=np.random.randint(0, 24))
    status = np.random.choice(['Open', 'In Progress', 'Awaiting Response', 'Resolved'], p=[0.1, 0.1, 0.1, 0.7])
    resolved = None
    if status == 'Resolved':
        resolved = (created + timedelta(hours=np.random.randint(1, 72))).strftime('%Y-%m-%dT%H:%M:%S')
    
    tickets.append({
        'ticket_id': f'TKT-{2800+i}',
        'customer_id': np.random.choice(customer_ids),
        'subject': np.random.choice(['Data export failing', 'API timeout issues', 'Dashboard UI glitch', 'Integration error', 'Billing question', 'Feature request']),
        'priority': np.random.choice(['Low', 'Medium', 'High', 'Critical'], p=[0.3, 0.4, 0.2, 0.1]),
        'status': status,
        'created_date': created.strftime('%Y-%m-%dT%H:%M:%S'),
        'resolved_date': resolved,
        'sentiment': np.random.choice(['Positive', 'Neutral', 'Negative'], p=[0.3, 0.5, 0.2])
    })
with open('data/tickets.json', 'w') as f:
    json.dump(tickets, f, indent=4)

# 3. Generate interactions.csv
num_interactions = 1000
interactions = pd.DataFrame({
    'interaction_id': [f'INT-{5000+i}' for i in range(num_interactions)],
    'customer_id': np.random.choice(customer_ids, num_interactions),
    'interaction_type': np.random.choice(['Login', 'Feature Usage', 'Support Call', 'QBR', 'Email Sent'], num_interactions),
    'description': ['System generated description' for _ in range(num_interactions)],
    'timestamp': [(datetime.now() - timedelta(days=np.random.randint(1, 60))).strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_interactions)]
})
interactions.to_csv('data/interactions.csv', index=False)

# 4. Generate churn_history.csv
num_churn = 50
churn_history = pd.DataFrame({
    'customer_id': [f'CHURN-{900+i}' for i in range(num_churn)],
    'churn_date': [(datetime.now() - timedelta(days=np.random.randint(1, 365))).strftime('%Y-%m-%d') for _ in range(num_churn)],
    'churn_reason': np.random.choice(['Price', 'Competitor', 'Support Quality', 'Feature Gap', 'Company Closed'], num_churn),
    'revenue_lost': np.random.randint(10000, 500000, num_churn)
})
churn_history.to_csv('data/churn_history.csv', index=False)

print("Generated all datasets successfully.")
