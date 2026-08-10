"""
ChurnGuard AI - Analytics Data Seeding Script
Purpose: Populate advanced analytics tables with realistic sample data
"""

import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "churnguard.db"


def seed_churn_predictions(conn):
    """Seed churn prediction data"""
    print("📊 Seeding churn predictions...")
    cursor = conn.cursor()
    
    # Get all customers
    cursor.execute("SELECT customer_id, risk_score FROM customers")
    customers = cursor.fetchall()
    
    predictions_data = []
    for customer_id, risk_score in customers:
        # Generate predictions for last 30 days
        for day in range(30):
            prediction_date = datetime.now() - timedelta(days=day)
            churn_prob = (risk_score + random.randint(-10, 10)) / 100.0
            churn_prob = max(0.0, min(1.0, churn_prob))  # Clamp between 0 and 1
            
            risk_factors = []
            if churn_prob > 0.7:
                risk_factors = ['Low Usage', 'Negative Sentiment', 'Open Critical Tickets']
            elif churn_prob > 0.5:
                risk_factors = ['Declining Engagement', 'Support Issues']
            else:
                risk_factors = ['Stable']
            
            predictions_data.append((
                customer_id,
                prediction_date.date(),
                churn_prob,
                str(risk_factors),
                random.uniform(0.7, 0.95),
                'v1.2.0',
                (prediction_date + timedelta(days=90)).date() if churn_prob > 0.7 else None
            ))
    
    cursor.executemany("""
        INSERT OR IGNORE INTO churn_predictions 
        (customer_id, prediction_date, churn_probability, risk_factors, 
         confidence_score, model_version, predicted_churn_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, predictions_data)
    
    print(f"   ✓ Inserted {len(predictions_data)} churn predictions")


def seed_health_history(conn):
    """Seed customer health history"""
    print("📈 Seeding health history...")
    cursor = conn.cursor()
    
    cursor.execute("SELECT customer_id, risk_score, health_status, arr FROM customers")
    customers = cursor.fetchall()
    
    history_data = []
    for customer_id, risk_score, health_status, arr in customers:
        # Generate history for last 90 days
        for day in range(90):
            snapshot_date = datetime.now() - timedelta(days=day)
            daily_risk = risk_score + random.randint(-5, 5)
            daily_risk = max(0, min(100, daily_risk))
            
            history_data.append((
                customer_id,
                snapshot_date.date(),
                daily_risk,
                health_status if daily_risk >= 75 else 'Low Risk',
                arr,
                random.randint(50, 500),
                random.randint(0, 5),
                random.randint(0, 2),
                random.uniform(-0.5, 0.8),
                random.uniform(40, 95),
                random.uniform(50, 98)
            ))
    
    cursor.executemany("""
        INSERT OR IGNORE INTO customer_health_history 
        (customer_id, snapshot_date, risk_score, health_status, arr,
         active_users, open_tickets, critical_tickets, sentiment_score,
         engagement_score, product_usage_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, history_data)
    
    print(f"   ✓ Inserted {len(history_data)} health history records")


def seed_interventions(conn):
    """Seed intervention actions"""
    print("🎯 Seeding intervention actions...")
    cursor = conn.cursor()
    
    cursor.execute("SELECT customer_id, risk_score FROM customers WHERE risk_score >= 60")
    high_risk_customers = cursor.fetchall()
    
    action_types = ['Executive Call', 'Account Review', 'Discount Offer', 
                   'Training Session', 'Feature Demo', 'Strategic Planning']
    
    interventions_data = []
    for customer_id, risk_score in high_risk_customers:
        num_actions = random.randint(1, 3)
        for _ in range(num_actions):
            initiated_date = datetime.now() - timedelta(days=random.randint(1, 60))
            completed_date = initiated_date + timedelta(days=random.randint(1, 14))
            status = random.choice(['Completed', 'In Progress', 'Planned'])
            
            risk_before = risk_score
            risk_after = risk_score - random.randint(5, 20) if status == 'Completed' else risk_score
            
            interventions_data.append((
                customer_id,
                random.choice(action_types),
                'CSM Team',
                initiated_date.date(),
                completed_date.date() if status == 'Completed' else None,
                status,
                'Successful' if status == 'Completed' and risk_after < risk_before else 'Pending',
                random.uniform(500, 5000),
                risk_before,
                risk_after if status == 'Completed' else None,
                'Standard intervention protocol applied'
            ))
    
    cursor.executemany("""
        INSERT INTO intervention_actions 
        (customer_id, action_type, initiated_by, initiated_date, completed_date,
         status, outcome, cost_estimate, risk_score_before, risk_score_after, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, interventions_data)
    
    print(f"   ✓ Inserted {len(interventions_data)} intervention actions")


def seed_nps_surveys(conn):
    """Seed NPS survey data"""
    print("⭐ Seeding NPS surveys...")
    cursor = conn.cursor()
    
    cursor.execute("SELECT customer_id FROM customers")
    customers = cursor.fetchall()
    
    nps_data = []
    for customer_id, in customers:
        # 2-3 surveys per customer
        num_surveys = random.randint(2, 3)
        for i in range(num_surveys):
            survey_date = datetime.now() - timedelta(days=random.randint(30, 180))
            nps_score = random.randint(0, 10)
            
            if nps_score <= 6:
                category = 'Detractor'
            elif nps_score <= 8:
                category = 'Passive'
            else:
                category = 'Promoter'
            
            feedback = {
                'Detractor': 'Needs improvement in support response time',
                'Passive': 'Product is good but could be better',
                'Promoter': 'Excellent product and support!'
            }
            
            nps_data.append((
                customer_id,
                None,
                survey_date.date(),
                nps_score,
                category,
                feedback[category],
                nps_score <= 6,
                False
            ))
    
    cursor.executemany("""
        INSERT INTO nps_surveys 
        (customer_id, stakeholder_id, survey_date, nps_score, nps_category,
         feedback_text, follow_up_required, follow_up_completed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, nps_data)
    
    print(f"   ✓ Inserted {len(nps_data)} NPS surveys")


def seed_revenue_events(conn):
    """Seed revenue events"""
    print("💰 Seeding revenue events...")
    cursor = conn.cursor()
    
    cursor.execute("SELECT customer_id, arr FROM customers")
    customers = cursor.fetchall()
    
    revenue_data = []
    for customer_id, current_arr in customers:
        # Initial customer event
        start_date = datetime.now() - timedelta(days=random.randint(365, 1095))
        revenue_data.append((
            customer_id,
            start_date.date(),
            'New Customer',
            0,
            current_arr * 0.8,
            current_arr * 0.8,
            'Initial contract signed',
            'Sales Team'
        ))
        
        # Possible expansion
        if random.random() > 0.6:
            expansion_date = start_date + timedelta(days=random.randint(180, 365))
            expansion_amount = current_arr * 0.2
            revenue_data.append((
                customer_id,
                expansion_date.date(),
                'Expansion',
                current_arr * 0.8,
                current_arr,
                expansion_amount,
                'Added more users and features',
                'CSM Team'
            ))
    
    cursor.executemany("""
        INSERT INTO revenue_events 
        (customer_id, event_date, event_type, previous_arr, new_arr,
         arr_change, reason, recorded_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, revenue_data)
    
    print(f"   ✓ Inserted {len(revenue_data)} revenue events")


def seed_feature_adoption(conn):
    """Seed feature adoption data"""
    print("🚀 Seeding feature adoption...")
    cursor = conn.cursor()
    
    features = [
        'Dashboard Analytics', 'Custom Reports', 'API Integration',
        'Mobile App', 'Automated Alerts', 'Data Export',
        'Team Collaboration', 'Advanced Security', 'SSO Login'
    ]
    
    cursor.execute("SELECT customer_id FROM customers")
    customers = cursor.fetchall()
    
    adoption_data = []
    for customer_id, in customers:
        for feature in features:
            if random.random() > 0.3:  # 70% adoption rate
                first_used = datetime.now() - timedelta(days=random.randint(1, 365))
                last_used = datetime.now() - timedelta(days=random.randint(0, 30))
                usage_count = random.randint(10, 500)
                
                statuses = ['Adopted', 'Power User', 'Exploring']
                status = random.choice(statuses)
                
                adoption_data.append((
                    customer_id,
                    feature,
                    first_used.date(),
                    last_used.date(),
                    usage_count,
                    status
                ))
    
    cursor.executemany("""
        INSERT INTO feature_adoption 
        (customer_id, feature_name, first_used_date, last_used_date,
         usage_count, adoption_status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, adoption_data)
    
    print(f"   ✓ Inserted {len(adoption_data)} feature adoption records")


def seed_contracts(conn):
    """Seed contract data"""
    print("📄 Seeding contracts...")
    cursor = conn.cursor()
    
    cursor.execute("SELECT customer_id, arr, renewal_date, tenure_months FROM customers")
    customers = cursor.fetchall()
    
    contract_data = []
    for customer_id, arr, renewal_date, tenure_months in customers:
        # Handle NULL tenure_months
        if tenure_months is None:
            tenure_months = random.randint(6, 36)
        
        start_date = datetime.now() - timedelta(days=tenure_months * 30)
        
        contract_data.append((
            customer_id,
            f'CNT-{customer_id:04d}-2024',
            start_date.date(),
            renewal_date,
            arr,
            random.choice(['Annually', 'Quarterly', 'Monthly']),
            True,
            'Net 30',
            'Active' if datetime.strptime(renewal_date, '%Y-%m-%d') > datetime.now() else 'Expiring Soon',
            start_date.date()
        ))
    
    cursor.executemany("""
        INSERT INTO contracts 
        (customer_id, contract_number, start_date, end_date, contract_value,
         billing_frequency, auto_renewal, payment_terms, contract_status, signed_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, contract_data)
    
    print(f"   ✓ Inserted {len(contract_data)} contracts")


def main():
    """Main seeding function"""
    print("🌱 Starting analytics data seeding...\n")
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        seed_churn_predictions(conn)
        seed_health_history(conn)
        seed_interventions(conn)
        seed_nps_surveys(conn)
        seed_revenue_events(conn)
        seed_feature_adoption(conn)
        seed_contracts(conn)
        
        conn.commit()
        print("\n✅ Analytics data seeding complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
