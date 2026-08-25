"""
ChurnGuard AI - Database Query Helper Module
Purpose: Reusable database queries for the Streamlit app
"""

import sqlite3
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
if not logger.handlers:
    logger.addHandler(handler)
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta


class ChurnGuardDB:
    """Database connection and query manager"""
    
    def __init__(self, db_path: str = "churnguard.db"):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = None) -> pd.DataFrame:
        """Execute query and return DataFrame"""
        conn = self.get_connection()
        try:
            if params:
                df = pd.read_sql_query(query, conn, params=params)
            else:
                df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            logger.error(f"Database query error: {e}")
            logger.debug(f"Failed query: {query} with params: {params}")
            return pd.DataFrame()
        finally:
            conn.close()
    
    def execute_write(self, query: str, params: tuple = None) -> int:
        """Execute INSERT/UPDATE/DELETE and return affected rows"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            logger.error(f"Database write error: {e}")
            logger.debug(f"Failed write: {query} with params: {params}")
            return 0
        finally:
            conn.close()
    
    # ========================================
    # CUSTOMER QUERIES
    # ========================================
    
    def get_high_risk_customers(self, min_risk_score: int = 75) -> pd.DataFrame:
        """Get customers with high churn risk"""
        query = """
        SELECT * FROM vw_high_risk_customers
        WHERE risk_score >= ?
        ORDER BY arr DESC
        """
        return self.execute_query(query, (min_risk_score,))
    
    def get_customer_details(self, customer_id: int) -> Dict[str, Any]:
        """Get detailed customer information"""
        query = """
        SELECT 
            c.*,
            COUNT(DISTINCT t.ticket_id) as total_tickets,
            COUNT(DISTINCT CASE WHEN t.status NOT IN ('Resolved', 'Closed') THEN t.ticket_id END) as open_tickets,
            COUNT(DISTINCT i.interaction_id) as total_interactions,
            MAX(i.interaction_date) as last_interaction,
            AVG(u.active_users) as avg_active_users
        FROM customers c
        LEFT JOIN tickets t ON c.customer_id = t.customer_id
        LEFT JOIN interactions i ON c.customer_id = i.customer_id
        LEFT JOIN usage_metrics u ON c.customer_id = u.customer_id
            AND u.metric_date >= date('now', '-30 days')
        WHERE c.customer_id = ?
        GROUP BY c.customer_id
        """
        df = self.execute_query(query, (customer_id,))
        return df.to_dict('records')[0] if not df.empty else {}
    
    def get_customers_by_health(self, health_status: str) -> pd.DataFrame:
        """Get customers filtered by health status"""
        query = """
        SELECT customer_id, company_name, risk_score, arr, 
               health_status, sentiment, last_activity
        FROM customers
        WHERE health_status = ?
        ORDER BY risk_score DESC
        """
        return self.execute_query(query, (health_status,))
    
    def get_renewal_pipeline(self, days_ahead: int = 90) -> pd.DataFrame:
        """Get customers with renewals in next N days"""
        query = """
        SELECT 
            c.customer_id,
            c.company_name,
            c.arr,
            c.risk_score,
            c.health_status,
            c.renewal_date,
            CAST(julianday(c.renewal_date) - julianday('now') AS INTEGER) as days_to_renewal,
            COUNT(DISTINCT t.ticket_id) as open_tickets
        FROM customers c
        LEFT JOIN tickets t ON c.customer_id = t.customer_id 
            AND t.status NOT IN ('Resolved', 'Closed')
        WHERE c.renewal_date BETWEEN date('now') AND date('now', '+' || ? || ' days')
        GROUP BY c.customer_id
        ORDER BY c.renewal_date ASC
        """
        return self.execute_query(query, (days_ahead,))
    
    # ========================================
    # TICKET QUERIES
    # ========================================
    
    def get_open_tickets(self, priority: Optional[str] = None) -> pd.DataFrame:
        """Get open tickets, optionally filtered by priority"""
        if priority:
            query = """
            SELECT t.*, c.company_name, c.risk_score as customer_risk
            FROM tickets t
            JOIN customers c ON t.customer_id = c.customer_id
            WHERE t.status NOT IN ('Resolved', 'Closed')
            AND t.priority = ?
            ORDER BY t.created_at DESC
            """
            return self.execute_query(query, (priority,))
        else:
            query = """
            SELECT t.*, c.company_name, c.risk_score as customer_risk
            FROM tickets t
            JOIN customers c ON t.customer_id = c.customer_id
            WHERE t.status NOT IN ('Resolved', 'Closed')
            ORDER BY t.created_at DESC
            """
            return self.execute_query(query)
    
    def get_ticket_metrics(self) -> Dict[str, Any]:
        """Get ticket summary metrics"""
        query = """
        SELECT 
            COUNT(*) as total_tickets,
            SUM(CASE WHEN status NOT IN ('Resolved', 'Closed') THEN 1 ELSE 0 END) as open_tickets,
            SUM(CASE WHEN priority = 'Critical' AND status NOT IN ('Resolved', 'Closed') THEN 1 ELSE 0 END) as critical_open,
            ROUND(AVG(CASE 
                WHEN resolved_at IS NOT NULL 
                THEN (julianday(resolved_at) - julianday(created_at)) * 24 
                ELSE NULL 
            END), 2) as avg_resolution_hours
        FROM tickets
        """
        df = self.execute_query(query)
        return df.to_dict('records')[0] if not df.empty else {}
    
    # ========================================
    # RISK ALERT QUERIES
    # ========================================
    
    def get_active_alerts(self, severity: Optional[str] = None) -> pd.DataFrame:
        """Get active risk alerts"""
        if severity:
            query = """
            SELECT ra.*, c.company_name, c.arr
            FROM risk_alerts ra
            JOIN customers c ON ra.customer_id = c.customer_id
            WHERE ra.is_resolved = 0
            AND ra.severity = ?
            ORDER BY ra.created_at DESC
            """
            return self.execute_query(query, (severity,))
        else:
            query = """
            SELECT ra.*, c.company_name, c.arr
            FROM risk_alerts ra
            JOIN customers c ON ra.customer_id = c.customer_id
            WHERE ra.is_resolved = 0
            ORDER BY ra.created_at DESC
            LIMIT 50
            """
            return self.execute_query(query)
    
    def resolve_alert(self, alert_id: int, resolved_by: str) -> int:
        """Mark an alert as resolved"""
        query = """
        UPDATE risk_alerts
        SET is_resolved = 1,
            resolved_at = CURRENT_TIMESTAMP,
            resolved_by = ?
        WHERE alert_id = ?
        """
        return self.execute_write(query, (resolved_by, alert_id))
    
    # ========================================
    # ANALYTICS QUERIES
    # ========================================
    
    def get_churn_rate_trend(self, days: int = 90) -> pd.DataFrame:
        """Get churn rate trend over time"""
        query = """
        SELECT 
            DATE(snapshot_date) as date,
            ROUND(AVG(risk_score), 2) as avg_risk_score,
            COUNT(CASE WHEN health_status = 'Critical' THEN 1 END) as critical_count,
            COUNT(CASE WHEN health_status = 'Medium' THEN 1 END) as medium_count,
            COUNT(CASE WHEN health_status = 'Low Risk' THEN 1 END) as low_risk_count
        FROM customer_health_history
        WHERE snapshot_date >= date('now', '-' || ? || ' days')
        GROUP BY DATE(snapshot_date)
        ORDER BY date DESC
        """
        return self.execute_query(query, (days,))
    
    def get_revenue_at_risk(self) -> float:
        """Calculate total revenue at risk"""
        query = """
        SELECT COALESCE(SUM(arr), 0.0) as total_at_risk
        FROM customers
        WHERE health_status IN ('Critical', 'Medium')
        """
        df = self.execute_query(query)
        if not df.empty and pd.notna(df['total_at_risk'].iloc[0]):
            return float(df['total_at_risk'].iloc[0])
        return 0.0
    
    def get_intervention_stats(self) -> pd.DataFrame:
        """Get intervention effectiveness statistics"""
        query = "SELECT * FROM vw_intervention_effectiveness"
        return self.execute_query(query)
    
    def get_nps_summary(self) -> pd.DataFrame:
        """Get NPS trends summary"""
        query = """
        SELECT * FROM vw_nps_trends
        WHERE survey_count > 0
        ORDER BY nps_score_calculated ASC
        """
        return self.execute_query(query)
    
    def get_usage_trends(self, customer_id: int, days: int = 30) -> pd.DataFrame:
        """Get usage trends for a specific customer"""
        query = """
        SELECT 
            metric_date,
            active_users,
            logins,
            feature_usage_score,
            api_calls,
            errors_count
        FROM usage_metrics
        WHERE customer_id = ?
        AND metric_date >= date('now', '-' || ? || ' days')
        ORDER BY metric_date DESC
        """
        return self.execute_query(query, (customer_id, days))
    
    def get_feature_adoption(self) -> pd.DataFrame:
        """Get feature adoption summary"""
        query = "SELECT * FROM vw_feature_adoption_summary"
        return self.execute_query(query)
    
    def get_at_risk_revenue_pipeline(self) -> pd.DataFrame:
        """Get at-risk revenue pipeline"""
        query = "SELECT * FROM vw_at_risk_revenue"
        return self.execute_query(query)
    
    # ========================================
    # DASHBOARD KPI QUERIES
    # ========================================
    
    def get_dashboard_kpis(self) -> Dict[str, Any]:
        """Get all KPIs for executive dashboard"""
        query = """
        SELECT 
            ROUND(AVG(risk_score), 1) as avg_risk_score,
            SUM(CASE WHEN health_status = 'Critical' THEN 1 ELSE 0 END) as critical_customers,
            SUM(CASE WHEN health_status = 'Medium' THEN 1 ELSE 0 END) as medium_customers,
            SUM(CASE WHEN health_status = 'Low Risk' THEN 1 ELSE 0 END) as low_risk_customers,
            SUM(CASE WHEN health_status IN ('Critical', 'Medium') THEN arr ELSE 0 END) as revenue_at_risk,
            SUM(arr) as total_arr,
            COUNT(*) as total_customers,
            ROUND(SUM(CASE WHEN health_status = 'Critical' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) as churn_rate
        FROM customers
        """
        df = self.execute_query(query)
        return df.to_dict('records')[0] if not df.empty else {}
    
    # ========================================
    # SEARCH & FILTER
    # ========================================
    
    def search_customers(self, search_term: str) -> pd.DataFrame:
        """Search customers by name"""
        query = """
        SELECT customer_id, company_name, risk_score, arr, health_status
        FROM customers
        WHERE company_name LIKE ?
        ORDER BY company_name
        """
        return self.execute_query(query, (f'%{search_term}%',))
    
    def search_tickets(self, search_term: str) -> pd.DataFrame:
        """Search tickets by subject or ID"""
        query = """
        SELECT t.*, c.company_name
        FROM tickets t
        JOIN customers c ON t.customer_id = c.customer_id
        WHERE t.subject LIKE ? OR t.ticket_id LIKE ?
        ORDER BY t.created_at DESC
        """
        search_pattern = f'%{search_term}%'
        return self.execute_query(query, (search_pattern, search_pattern))


# ========================================
# EXAMPLE USAGE
# ========================================

if __name__ == "__main__":
    db = ChurnGuardDB()
    
    # Test queries
    print("High Risk Customers:")
    print(db.get_high_risk_customers(75))
    
    print("\nDashboard KPIs:")
    print(db.get_dashboard_kpis())
    
    print("\nActive Alerts:")
    print(db.get_active_alerts())
