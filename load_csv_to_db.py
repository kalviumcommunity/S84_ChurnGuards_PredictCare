"""
Load CSV/JSON data into SQLite database
This bridges CSV files -> Database
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime

def load_csv_data_to_database():
    """Load all CSV/JSON files into the database"""
    
    conn = sqlite3.connect('churnguard.db')
    cursor = conn.cursor()
    
    print("🔄 Loading CSV data into database...")
    
    # ========================================
    # 1. LOAD CUSTOMERS
    # ========================================
    try:
        customers_df = pd.read_csv('data/customers.csv')
        print(f"📊 Loaded {len(customers_df)} customers from CSV")
        
        # Clear existing data
        cursor.execute("DELETE FROM customers")
        
        # Insert customers
        for _, row in customers_df.iterrows():
            cursor.execute("""
                INSERT INTO customers (
                    company_name, industry, arr, 
                    renewal_date,
                    health_status, risk_score, sentiment
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row['company_name'],
                row['industry'],
                int(row['arr']),
                row['renewal_date'],
                'Low Risk',  # Default, will calculate later
                20,  # Default risk score
                'Neutral'  # Default sentiment
            ))
        
        print(f"✓ Inserted {len(customers_df)} customers")
        
    except Exception as e:
        print(f"❌ Error loading customers: {e}")
    
    # ========================================
    # 2. LOAD TICKETS
    # ========================================
    try:
        with open('data/tickets.json', 'r') as f:
            tickets_data = json.load(f)
        
        print(f"🎫 Loaded {len(tickets_data)} tickets from JSON")
        
        # Clear existing tickets
        cursor.execute("DELETE FROM tickets")
        
        # Insert tickets
        for ticket in tickets_data:
            # Map customer_id from CSV format to integer
            cust_id_str = ticket['customer_id']
            if isinstance(cust_id_str, str) and 'CUST-' in cust_id_str:
                cust_id = int(cust_id_str.replace('CUST-', ''))
            else:
                cust_id = 1  # Default fallback
            
            cursor.execute("""
                INSERT INTO tickets (
                    ticket_id, customer_id, subject, description,
                    priority, status, sentiment, category,
                    created_at, resolved_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ticket['ticket_id'],
                cust_id,
                ticket['subject'],
                ticket.get('subject', 'No description'),  # Use subject as description
                ticket['priority'],
                ticket['status'],
                ticket['sentiment'],
                'Support',  # Default category
                ticket['created_date'],
                ticket.get('resolved_date')
            ))
        
        print(f"✓ Inserted {len(tickets_data)} tickets")
        
    except Exception as e:
        print(f"❌ Error loading tickets: {e}")
    
    # ========================================
    # 3. LOAD INTERACTIONS
    # ========================================
    try:
        interactions_df = pd.read_csv('data/interactions.csv')
        print(f"💬 Loaded {len(interactions_df)} interactions from CSV")
        
        # Clear existing interactions
        cursor.execute("DELETE FROM interactions")
        
        # Insert interactions
        for _, row in interactions_df.iterrows():
            # Map customer_id
            cust_id_str = row['customer_id']
            if isinstance(cust_id_str, str) and 'CUST-' in cust_id_str:
                cust_id = int(cust_id_str.replace('CUST-', ''))
            else:
                cust_id = 1
            
            # Map interaction types
            interaction_type = row['interaction_type']
            type_mapping = {
                'Login': 'Email',
                'Feature Usage': 'Training',
                'Support Call': 'Call',
                'QBR': 'QBR',
                'Email Sent': 'Email'
            }
            mapped_type = type_mapping.get(interaction_type, 'Email')
            
            cursor.execute("""
                INSERT INTO interactions (
                    customer_id, interaction_type,
                    interaction_date, notes
                ) VALUES (?, ?, ?, ?)
            """, (
                cust_id,
                mapped_type,
                row['timestamp'],
                row['description']
            ))
        
        print(f"✓ Inserted {len(interactions_df)} interactions")
        
    except Exception as e:
        print(f"❌ Error loading interactions: {e}")
    
    # ========================================
    # 4. UPDATE RISK SCORES FROM FEATURE ENGINEERING
    # ========================================
    try:
        print("\n🧮 Calculating risk scores...")
        
        from scripts.data_ingestion import load_data as load_raw
        from scripts.data_cleaning import clean_data
        from scripts.feature_engineering import engineer_features
        
        customers, tickets, interactions, churn_history = load_raw('data')
        customers, tickets, interactions, churn_history = clean_data(customers, tickets, interactions, churn_history)
        customers, tickets = engineer_features(customers, tickets, interactions)
        
        # Update customers with calculated risk scores
        for _, row in customers.iterrows():
            # Find matching customer in database by company name
            cursor.execute("""
                UPDATE customers
                SET risk_score = ?,
                    health_status = ?
                WHERE company_name = ?
            """, (
                int(row.get('risk_score', 20)),
                row.get('health_status', 'Low Risk'),
                row['company_name']
            ))
        
        print(f"✓ Updated risk scores for {len(customers)} customers")
        
    except Exception as e:
        print(f"⚠️ Could not calculate risk scores: {e}")
    
    # Commit all changes
    conn.commit()
    conn.close()
    
    print("\n✅ CSV data successfully loaded into database!")
    print("📂 Database: churnguard.db")
    
    # Verify
    conn = sqlite3.connect('churnguard.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tickets")
    ticket_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM interactions")
    interaction_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n📊 Database contains:")
    print(f"   - {customer_count} customers")
    print(f"   - {ticket_count} tickets")
    print(f"   - {interaction_count} interactions")


if __name__ == "__main__":
    load_csv_data_to_database()
