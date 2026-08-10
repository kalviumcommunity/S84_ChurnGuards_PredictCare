"""
Data Snapshot Manager
Handles version history for uploaded data
Allows users to switch between historical data snapshots
"""

import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional


class SnapshotManager:
    """Manage data snapshots and version history"""
    
    def __init__(self, db_path: str = "churnguard.db"):
        self.db_path = db_path
        self._ensure_snapshot_tables()
    
    def _ensure_snapshot_tables(self):
        """Create snapshot tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Read and execute snapshot schema
        try:
            with open('database_snapshots.sql', 'r') as f:
                snapshot_schema = f.read()
                cursor.executescript(snapshot_schema)
            conn.commit()
        except FileNotFoundError:
            print("⚠️ Snapshot schema file not found, creating tables manually...")
            # Create tables manually as fallback
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS data_snapshots (
                    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_name VARCHAR(255) NOT NULL,
                    snapshot_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    customer_count INTEGER,
                    ticket_count INTEGER,
                    interaction_count INTEGER,
                    uploaded_by VARCHAR(100),
                    notes TEXT,
                    is_active BOOLEAN DEFAULT 0
                );
                
                CREATE TABLE IF NOT EXISTS customers_history (
                    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_id INTEGER NOT NULL,
                    customer_id INTEGER,
                    company_name VARCHAR(255),
                    industry VARCHAR(100),
                    arr DECIMAL(12, 2),
                    risk_score INTEGER,
                    health_status VARCHAR(20),
                    sentiment VARCHAR(20),
                    renewal_date DATE,
                    last_activity TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS tickets_history (
                    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_id INTEGER NOT NULL,
                    ticket_id VARCHAR(50),
                    customer_id INTEGER,
                    subject TEXT,
                    priority VARCHAR(20),
                    status VARCHAR(50),
                    sentiment VARCHAR(20),
                    created_at TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS interactions_history (
                    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_id INTEGER NOT NULL,
                    customer_id INTEGER,
                    interaction_type VARCHAR(50),
                    interaction_date TIMESTAMP,
                    notes TEXT
                );
            """)
            conn.commit()
        
        conn.close()
    
    def create_snapshot(self, snapshot_name: str, uploaded_by: str = "User", notes: str = "") -> int:
        """
        Create a new snapshot of current data
        Returns snapshot_id
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get current data counts
            cursor.execute("SELECT COUNT(*) FROM customers")
            customer_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tickets")
            ticket_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM interactions")
            interaction_count = cursor.fetchone()[0]
            
            # Deactivate all previous snapshots
            cursor.execute("UPDATE data_snapshots SET is_active = 0")
            
            # Create new snapshot record
            cursor.execute("""
                INSERT INTO data_snapshots (
                    snapshot_name, customer_count, ticket_count, 
                    interaction_count, uploaded_by, notes, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (snapshot_name, customer_count, ticket_count, interaction_count, uploaded_by, notes))
            
            snapshot_id = cursor.lastrowid
            
            # Copy current customers to history
            cursor.execute("""
                INSERT INTO customers_history (
                    snapshot_id, customer_id, company_name, industry, arr,
                    risk_score, health_status, sentiment, renewal_date, last_activity
                )
                SELECT ?, customer_id, company_name, industry, arr,
                       risk_score, health_status, sentiment, renewal_date, last_activity
                FROM customers
            """, (snapshot_id,))
            
            # Copy current tickets to history
            cursor.execute("""
                INSERT INTO tickets_history (
                    snapshot_id, ticket_id, customer_id, subject, 
                    priority, status, sentiment, created_at
                )
                SELECT ?, ticket_id, customer_id, subject,
                       priority, status, sentiment, created_at
                FROM tickets
            """, (snapshot_id,))
            
            # Copy current interactions to history
            cursor.execute("""
                INSERT INTO interactions_history (
                    snapshot_id, customer_id, interaction_type,
                    interaction_date, notes
                )
                SELECT ?, customer_id, interaction_type,
                       interaction_date, notes
                FROM interactions
            """, (snapshot_id,))
            
            conn.commit()
            print(f"✅ Created snapshot: {snapshot_name} (ID: {snapshot_id})")
            return snapshot_id
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error creating snapshot: {e}")
            return -1
        finally:
            conn.close()
    
    def get_all_snapshots(self) -> pd.DataFrame:
        """Get list of all snapshots"""
        conn = sqlite3.connect(self.db_path)
        query = """
            SELECT 
                snapshot_id,
                snapshot_name,
                snapshot_date,
                customer_count,
                ticket_count,
                interaction_count,
                uploaded_by,
                is_active,
                CASE WHEN is_active = 1 THEN '✓ Active' ELSE 'Archived' END as status
            FROM data_snapshots
            ORDER BY snapshot_date DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_active_snapshot_id(self) -> Optional[int]:
        """Get the currently active snapshot ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT snapshot_id FROM data_snapshots WHERE is_active = 1 LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def set_active_snapshot(self, snapshot_id: int) -> bool:
        """Switch to a different snapshot (makes it active)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Deactivate all snapshots
            cursor.execute("UPDATE data_snapshots SET is_active = 0")
            
            # Activate selected snapshot
            cursor.execute("UPDATE data_snapshots SET is_active = 1 WHERE snapshot_id = ?", (snapshot_id,))
            
            conn.commit()
            print(f"✅ Switched to snapshot ID: {snapshot_id}")
            return True
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error switching snapshot: {e}")
            return False
        finally:
            conn.close()
    
    def load_snapshot_data(self, snapshot_id: int) -> Dict[str, pd.DataFrame]:
        """
        Load data from a specific snapshot
        Returns dict with customers, tickets, interactions DataFrames
        """
        conn = sqlite3.connect(self.db_path)
        
        # Load customers from snapshot
        customers = pd.read_sql_query("""
            SELECT * FROM customers_history 
            WHERE snapshot_id = ?
        """, conn, params=(snapshot_id,))
        
        # Load tickets from snapshot
        tickets = pd.read_sql_query("""
            SELECT * FROM tickets_history 
            WHERE snapshot_id = ?
        """, conn, params=(snapshot_id,))
        
        # Load interactions from snapshot
        interactions = pd.read_sql_query("""
            SELECT * FROM interactions_history 
            WHERE snapshot_id = ?
        """, conn, params=(snapshot_id,))
        
        conn.close()
        
        return {
            'customers': customers,
            'tickets': tickets,
            'interactions': interactions
        }
    
    def delete_snapshot(self, snapshot_id: int) -> bool:
        """Delete a snapshot and its associated history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Delete history records
            cursor.execute("DELETE FROM customers_history WHERE snapshot_id = ?", (snapshot_id,))
            cursor.execute("DELETE FROM tickets_history WHERE snapshot_id = ?", (snapshot_id,))
            cursor.execute("DELETE FROM interactions_history WHERE snapshot_id = ?", (snapshot_id,))
            
            # Delete snapshot record
            cursor.execute("DELETE FROM data_snapshots WHERE snapshot_id = ?", (snapshot_id,))
            
            conn.commit()
            print(f"✅ Deleted snapshot ID: {snapshot_id}")
            return True
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error deleting snapshot: {e}")
            return False
        finally:
            conn.close()
    
    def get_snapshot_comparison(self, snapshot_id1: int, snapshot_id2: int) -> Dict[str, Any]:
        """Compare two snapshots and return statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get snapshot 1 stats
        cursor.execute("""
            SELECT customer_count, ticket_count, interaction_count, snapshot_name, snapshot_date
            FROM data_snapshots WHERE snapshot_id = ?
        """, (snapshot_id1,))
        snap1 = cursor.fetchone()
        
        # Get snapshot 2 stats
        cursor.execute("""
            SELECT customer_count, ticket_count, interaction_count, snapshot_name, snapshot_date
            FROM data_snapshots WHERE snapshot_id = ?
        """, (snapshot_id2,))
        snap2 = cursor.fetchone()
        
        conn.close()
        
        if not snap1 or not snap2:
            return {}
        
        return {
            'snapshot1': {
                'name': snap1[3],
                'date': snap1[4],
                'customers': snap1[0],
                'tickets': snap1[1],
                'interactions': snap1[2]
            },
            'snapshot2': {
                'name': snap2[3],
                'date': snap2[4],
                'customers': snap2[0],
                'tickets': snap2[1],
                'interactions': snap2[2]
            },
            'diff': {
                'customers': snap2[0] - snap1[0],
                'tickets': snap2[1] - snap1[1],
                'interactions': snap2[2] - snap1[2]
            }
        }


# Example usage
if __name__ == "__main__":
    manager = SnapshotManager()
    
    # Create a snapshot
    snapshot_id = manager.create_snapshot("Initial Data Upload", "Admin", "First data load")
    
    # List all snapshots
    print("\n📊 All Snapshots:")
    print(manager.get_all_snapshots())
    
    # Load data from snapshot
    data = manager.load_snapshot_data(snapshot_id)
    print(f"\n✅ Loaded {len(data['customers'])} customers from snapshot")
