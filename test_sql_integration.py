import sys
if hasattr(sys.stdout, 'encoding') and sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from db_queries import ChurnGuardDB
import pandas as pd

def test_sql_integration():
    """Test all SQL query functions"""
    
    print("=" * 60)
    print("🔍 TESTING SQL QUERY INTEGRATION (Module 2.38-2.40)")
    print("=" * 60)
    
    db = ChurnGuardDB('churnguard.db')
    
    print("\n✅ Test 1: get_dashboard_kpis()")
    print("-" * 60)
    kpis = db.get_dashboard_kpis()
    print(f"Result type: {type(kpis)}")
    print(f"KPIs: {kpis}")
    assert isinstance(kpis, dict), "KPIs should be a dictionary"
    assert 'total_customers' in kpis, "Should have total_customers"
    print(f"✓ Total Customers: {kpis['total_customers']}")
    print(f"✓ Average Risk Score: {kpis['avg_risk_score']}")
    print(f"✓ Revenue at Risk: ${kpis['revenue_at_risk']:,.2f}")
    
    print("\n✅ Test 2: get_high_risk_customers(70)")
    print("-" * 60)
    high_risk = db.get_high_risk_customers(min_risk_score=70)
    print(f"Result type: {type(high_risk)}")
    print(f"Found {len(high_risk)} high-risk customers")
    assert isinstance(high_risk, pd.DataFrame), "Should return DataFrame"
    if not high_risk.empty:
        print(f"✓ Highest risk score: {high_risk['risk_score'].max()}")
        print(f"✓ Total ARR at risk: ${high_risk['arr'].sum():,.2f}")
    else:
        print("✓ No customers above threshold 70 (this is OK)")
    
    print("\n✅ Test 3: get_open_tickets()")
    print("-" * 60)
    tickets = db.get_open_tickets()
    print(f"Result type: {type(tickets)}")
    print(f"Found {len(tickets)} open tickets")
    assert isinstance(tickets, pd.DataFrame), "Should return DataFrame"
    if not tickets.empty:
        print(f"✓ Ticket priorities: {tickets['priority'].value_counts().to_dict()}")
    else:
        print("✓ No open tickets (all resolved)")
    
    print("\n✅ Test 4: get_open_tickets(priority='Critical')")
    print("-" * 60)
    critical_tickets = db.get_open_tickets(priority='Critical')
    print(f"Found {len(critical_tickets)} critical open tickets")
    assert isinstance(critical_tickets, pd.DataFrame), "Should return DataFrame"
    print(f"✓ Critical tickets count: {len(critical_tickets)}")
    
    print("\n✅ Test 5: get_ticket_metrics()")
    print("-" * 60)
    metrics = db.get_ticket_metrics()
    print(f"Result type: {type(metrics)}")
    print(f"Ticket Metrics: {metrics}")
    assert isinstance(metrics, dict), "Should be a dictionary"
    if metrics:
        print(f"✓ Total Tickets: {metrics.get('total_tickets', 0)}")
        print(f"✓ Open Tickets: {metrics.get('open_tickets', 0)}")
        print(f"✓ Critical Open: {metrics.get('critical_open', 0)}")
    
    print("\n✅ Test 6: get_revenue_at_risk()")
    print("-" * 60)
    revenue = db.get_revenue_at_risk()
    print(f"Result type: {type(revenue)}")
    print(f"Revenue at Risk: ${revenue:,.2f}")
    assert isinstance(revenue, (int, float)) or hasattr(revenue, '__float__'), "Should be a number"
    print(f"✓ Revenue calculation successful")
    
    print("\n✅ Test 7: search_customers('Company')")
    print("-" * 60)
    search_results = db.search_customers('Company')
    print(f"Found {len(search_results)} customers matching 'Company'")
    assert isinstance(search_results, pd.DataFrame), "Should return DataFrame"
    if not search_results.empty:
        print(f"✓ First 3 results:")
        for _, row in search_results.head(3).iterrows():
            print(f"  - {row['company_name']} (Risk: {row['risk_score']})")
    
    print("\n✅ Test 8: get_renewal_pipeline(90)")
    print("-" * 60)
    renewals = db.get_renewal_pipeline(days_ahead=90)
    print(f"Found {len(renewals)} customers with renewals in next 90 days")
    assert isinstance(renewals, pd.DataFrame), "Should return DataFrame"
    if not renewals.empty:
        print(f"✓ Upcoming renewals: {len(renewals)}")
        print(f"✓ Total renewal ARR: ${renewals['arr'].sum():,.2f}")
    
    print("\n" + "=" * 60)
    print("✅ ALL SQL QUERY INTEGRATION TESTS PASSED!")
    print("=" * 60)
    print("\n📊 Summary:")
    print(f"  ✓ Tested 8 SQL query functions")
    print(f"  ✓ All functions return correct data types")
    print(f"  ✓ Database queries execute successfully")
    print(f"  ✓ Module 2.38-2.40 COMPLETE")
    print("\n🎉 SQL Integration is working perfectly!")


if __name__ == "__main__":
    test_sql_integration()
