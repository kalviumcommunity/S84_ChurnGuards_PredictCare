import sys
if hasattr(sys.stdout, 'encoding') and sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import sqlite3
import pandas as pd

def verify_database():
    conn = sqlite3.connect('churnguard.db')
    cursor = conn.cursor()
    
    print("=" * 60)
    print("📊 CHURNGUARD DATABASE VERIFICATION")
    print("=" * 60)
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print(f"\n✅ Total Tables Created: {len(tables)}")
    print("\n📋 Table List:")
    for table in tables:
        print(f"  ✓ {table[0]}")
    
    print("\n" + "=" * 60)
    print("📈 DATA COUNTS")
    print("=" * 60)
    
    # Core tables
    print("\n🔹 Core Tables:")
    cursor.execute("SELECT COUNT(*) FROM customers")
    print(f"  Customers: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM tickets")
    print(f"  Tickets: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM interactions")
    print(f"  Interactions: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM usage_metrics")
    print(f"  Usage Metrics: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM risk_alerts")
    print(f"  Risk Alerts: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM stakeholders")
    print(f"  Stakeholders: {cursor.fetchone()[0]}")
    
    # Analytics tables
    print("\n🔹 Analytics Tables:")
    cursor.execute("SELECT COUNT(*) FROM churn_predictions")
    print(f"  Churn Predictions: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM customer_health_history")
    print(f"  Health History: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM intervention_actions")
    print(f"  Intervention Actions: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM nps_surveys")
    print(f"  NPS Surveys: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM revenue_events")
    print(f"  Revenue Events: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM feature_adoption")
    print(f"  Feature Adoption: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM contracts")
    print(f"  Contracts: {cursor.fetchone()[0]}")
    
    # Snapshot tables
    print("\n🔹 Version History:")
    cursor.execute("SELECT COUNT(*) FROM data_snapshots")
    print(f"  Snapshots: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM customers_history")
    print(f"  Customer History Records: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM tickets_history")
    print(f"  Ticket History Records: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM interactions_history")
    print(f"  Interaction History Records: {cursor.fetchone()[0]}")
    
    # Sample data
    print("\n" + "=" * 60)
    print("🔍 SAMPLE DATA")
    print("=" * 60)
    
    print("\n🔹 Top 5 High-Risk Customers:")
    df = pd.read_sql_query("""
        SELECT company_name, risk_score, health_status, arr
        FROM customers
        WHERE health_status = 'Critical'
        ORDER BY risk_score DESC
        LIMIT 5
    """, conn)
    print(df.to_string(index=False))
    
    print("\n🔹 Open Critical Tickets:")
    cursor.execute("""
        SELECT COUNT(*) FROM tickets 
        WHERE status NOT IN ('Resolved', 'Closed') 
        AND priority = 'Critical'
    """)
    print(f"  Count: {cursor.fetchone()[0]}")
    
    print("\n🔹 Recent Snapshots:")
    df = pd.read_sql_query("""
        SELECT snapshot_name, snapshot_date, customer_count, 
               is_active, uploaded_by
        FROM data_snapshots
        ORDER BY snapshot_date DESC
        LIMIT 3
    """, conn)
    if not df.empty:
        print(df.to_string(index=False))
    else:
        print("  No snapshots yet")
    
    print("\n" + "=" * 60)
    print("✅ DATABASE VERIFICATION COMPLETE!")
    print("=" * 60)
    
    conn.close()

if __name__ == "__main__":
    verify_database()
