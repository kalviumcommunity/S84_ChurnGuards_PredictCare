"""
ChurnGuard AI - Database Initialization Script
Purpose: Create and populate the SQLite database with schema and sample data
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

# Database configuration
DB_PATH = "churnguard.db"
SCHEMA_FILE = "database_schema.sql"


def init_database():
    """Initialize database with schema"""
    print("🔧 Initializing ChurnGuard database...")
    
    # Remove existing database if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"   Removed existing database: {DB_PATH}")
    
    # Create connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read and execute main schema
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    cursor.executescript(schema_sql)
    print(f"   ✓ Schema created from {SCHEMA_FILE}")
    
    # Execute triggers
    if os.path.exists("database_triggers.sql"):
        with open("database_triggers.sql", 'r', encoding='utf-8') as f:
            triggers_sql = f.read()
        cursor.executescript(triggers_sql)
        print(f"   ✓ Triggers created from database_triggers.sql")
    
    # Execute analytics schema
    if os.path.exists("database_analytics.sql"):
        with open("database_analytics.sql", 'r', encoding='utf-8') as f:
            analytics_sql = f.read()
        cursor.executescript(analytics_sql)
        print(f"   ✓ Analytics schema created from database_analytics.sql")
        
    # Execute snapshots schema
    if os.path.exists("database_snapshots.sql"):
        with open("database_snapshots.sql", 'r', encoding='utf-8') as f:
            snapshots_sql = f.read()
        cursor.executescript(snapshots_sql)
        print(f"   ✓ Snapshots schema created from database_snapshots.sql")
    
    conn.commit()
    return conn


def seed_sample_data(conn):
    """Insert sample data for testing"""
    print("📊 Seeding sample data...")
    cursor = conn.cursor()
    
    # Sample customers
    customers_data = [
        ('Acme Corp', 'Technology', '5000+', 1200000, 85, 'Critical', 'Negative', 36, '2026-10-15'),
        ('TechFlow Inc', 'SaaS', '1000-5000', 850000, 78, 'Critical', 'Neutral', 24, '2026-11-20'),
        ('GlobalNet', 'Finance', '500-1000', 620000, 88, 'Critical', 'Negative', 18, '2026-09-30'),
        ('DataSync Ltd', 'Healthcare', '100-500', 450000, 45, 'Low Risk', 'Positive', 48, '2027-02-15'),
        ('CloudBase Systems', 'Retail', '1000-5000', 980000, 52, 'Medium', 'Neutral', 30, '2027-01-10'),
    ]
    
    for customer in customers_data:
        cursor.execute("""
            INSERT INTO customers (company_name, industry, company_size, arr, risk_score, 
                                   health_status, sentiment, tenure_months, renewal_date, last_activity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (*customer, datetime.now() - timedelta(days=random.randint(1, 10))))
    
    print(f"   ✓ Inserted {len(customers_data)} customers")
    
    # Sample tickets
    tickets_data = [
        ('TKT-2842', 1, 'Data export failing on Q3 Reports', 'Export timeout issue', 'Critical', 'Open', 'Bug', 85, 'Negative'),
        ('TKT-2843', 1, 'API timeout issues', 'Intermittent API failures', 'High', 'In Progress', 'Bug', 75, 'Negative'),
        ('TKT-2844', 2, 'Integration error with CRM', 'Unable to sync data', 'High', 'Open', 'Integration', 78, 'Neutral'),
        ('TKT-2845', 3, 'Dashboard UI glitch', 'Layout broken on mobile', 'Medium', 'Resolved', 'UI', 45, 'Neutral'),
        ('TKT-2846', 4, 'Feature request: Custom reports', 'Need more reporting options', 'Low', 'Open', 'Feature', 30, 'Positive'),
    ]
    
    for ticket in tickets_data:
        cursor.execute("""
            INSERT INTO tickets (ticket_id, customer_id, subject, description, priority, 
                                status, category, risk_score, sentiment, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (*ticket, datetime.now() - timedelta(hours=random.randint(1, 48))))
    
    print(f"   ✓ Inserted {len(tickets_data)} tickets")
    
    # Sample interactions
    interactions_data = [
        (1, 'Email', 'Negative', 'Complaint about export failures'),
        (1, 'Call', 'Neutral', 'Status update on ticket'),
        (2, 'QBR', 'Neutral', 'Quarterly business review'),
        (3, 'Meeting', 'Negative', 'Escalation meeting'),
        (4, 'Call', 'Positive', 'Product feedback session'),
    ]
    
    for interaction in interactions_data:
        cursor.execute("""
            INSERT INTO interactions (customer_id, interaction_type, interaction_date, 
                                     sentiment, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (interaction[0], interaction[1], datetime.now() - timedelta(days=random.randint(1, 30)), 
              interaction[2], interaction[3]))
    
    print(f"   ✓ Inserted {len(interactions_data)} interactions")
    
    # Sample usage metrics
    for customer_id in range(1, 6):
        for day in range(30):
            metric_date = datetime.now() - timedelta(days=day)
            cursor.execute("""
                INSERT INTO usage_metrics (customer_id, metric_date, active_users, logins, 
                                          feature_usage_score, api_calls)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (customer_id, metric_date.date(), 
                  random.randint(50, 500), random.randint(100, 1000),
                  random.uniform(60, 95), random.randint(500, 5000)))
    
    print(f"   ✓ Inserted usage metrics for 5 customers (30 days)")
    
    # Sample risk alerts
    alerts_data = [
        (1, 'Usage Drop', 'Critical', 'Active users dropped by 22% in last 7 days'),
        (1, 'Negative Sentiment', 'High', 'Multiple negative support interactions detected'),
        (2, 'Renewal Risk', 'High', 'Renewal date approaching with unresolved escalations'),
        (3, 'Stakeholder Departure', 'Critical', 'Key sponsor departed the organization'),
    ]
    
    for alert in alerts_data:
        cursor.execute("""
            INSERT INTO risk_alerts (customer_id, alert_type, severity, message)
            VALUES (?, ?, ?, ?)
        """, alert)
    
    print(f"   ✓ Inserted {len(alerts_data)} risk alerts")
    
    # Sample stakeholders
    stakeholders_data = [
        (1, 'Sarah Jenkins', 'sarah.jenkins@acmecorp.com', 'VP Operations', 'Operations', 'Champion'),
        (1, 'Mike Chen', 'mike.chen@acmecorp.com', 'IT Manager', 'Technology', 'High'),
        (2, 'Elena Rodriguez', 'elena@techflow.com', 'CEO', 'Executive', 'Champion'),
        (3, 'David Park', 'david@globalnet.com', 'CFO', 'Finance', 'High'),
        (4, 'Lisa Wang', 'lisa@datasync.com', 'Product Manager', 'Product', 'Medium'),
    ]
    
    for stakeholder in stakeholders_data:
        cursor.execute("""
            INSERT INTO stakeholders (customer_id, name, email, role, department, influence_level, last_contact_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (*stakeholder, datetime.now().date() - timedelta(days=random.randint(1, 30))))
    
    print(f"   ✓ Inserted {len(stakeholders_data)} stakeholders")
    
    conn.commit()


def verify_database(conn):
    """Verify database structure and data"""
    print("\n✅ Verifying database...")
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"   Tables created: {len(tables)}")
    
    # Check views
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
    views = cursor.fetchall()
    print(f"   Views created: {len(views)}")
    
    # Check record counts
    tables_to_check = ['customers', 'tickets', 'interactions', 'usage_metrics', 'risk_alerts', 'stakeholders']
    for table in tables_to_check:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   {table}: {count} records")
    
    print("\n🎉 Database initialization complete!")
    print(f"   Database file: {DB_PATH}")


if __name__ == "__main__":
    try:
        conn = init_database()
        seed_sample_data(conn)
        verify_database(conn)
        conn.close()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
