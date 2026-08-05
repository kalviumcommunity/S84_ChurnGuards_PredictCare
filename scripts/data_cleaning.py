import pandas as pd

def clean_data(customers, tickets, interactions, churn_history):
    """
    Cleans data (handles dates, missing values).
    """
    # Clean customers
    if not customers.empty:
        customers['renewal_date'] = pd.to_datetime(customers['renewal_date'])
        
    # Clean tickets
    if not tickets.empty:
        tickets['created_date'] = pd.to_datetime(tickets['created_date'])
        tickets['resolved_date'] = pd.to_datetime(tickets['resolved_date'])
        
    # Clean interactions
    if not interactions.empty:
        interactions['timestamp'] = pd.to_datetime(interactions['timestamp'])
        
    # Clean churn history
    if not churn_history.empty:
        churn_history['churn_date'] = pd.to_datetime(churn_history['churn_date'])
        
    return customers, tickets, interactions, churn_history
