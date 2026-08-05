import pandas as pd
import json

def load_data(data_dir='data'):
    """
    Loads raw data from CSV and JSON files.
    """
    # Load customers
    try:
        customers = pd.read_csv(f'{data_dir}/customers.csv')
    except FileNotFoundError:
        customers = pd.DataFrame()
        
    # Load tickets
    try:
        with open(f'{data_dir}/tickets.json', 'r') as f:
            tickets_data = json.load(f)
        tickets = pd.DataFrame(tickets_data)
    except FileNotFoundError:
        tickets = pd.DataFrame()
        
    # Load interactions
    try:
        interactions = pd.read_csv(f'{data_dir}/interactions.csv')
    except FileNotFoundError:
        interactions = pd.DataFrame()
        
    # Load churn history
    try:
        churn_history = pd.read_csv(f'{data_dir}/churn_history.csv')
    except FileNotFoundError:
        churn_history = pd.DataFrame()
        
    return customers, tickets, interactions, churn_history
