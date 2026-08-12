"""
Automated Data Pipeline for ChurnGuard AI
Module 2.58: Complete ETL Pipeline Automation

Usage:
    python run_pipeline.py                    # Run full pipeline
    python run_pipeline.py --data-dir data/   # Specify data directory
    python run_pipeline.py --skip-generate    # Use existing data
    python run_pipeline.py --verify-only      # Only verify, don't rebuild
"""

import argparse
import sys
import os
from datetime import datetime
import sqlite3
import pandas as pd


class ChurnGuardPipeline:
    """Automated data pipeline orchestrator"""
    
    def __init__(self, data_dir='data', db_path='churnguard.db'):
        self.data_dir = data_dir
        self.db_path = db_path
        self.start_time = datetime.now()
        self.logs = []
        
    def log(self, message, level="INFO"):
        """Log pipeline progress"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        
        # Color coding
        if level == "SUCCESS":
            print(f"\033[92m{log_entry}\033[0m")  # Green
        elif level == "ERROR":
            print(f"\033[91m{log_entry}\033[0m")  # Red
        elif level == "WARNING":
            print(f"\033[93m{log_entry}\033[0m")  # Yellow
        else:
            print(log_entry)
    
    def print_header(self, text):
        """Print section header"""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)
    
    def step_1_validate_environment(self):
        """Validate required files and dependencies"""
        self.print_header("STEP 1: Validating Environment")
        
        required_files = [
            'database_schema.sql',
            'database_analytics.sql',
            'db_queries.py',
            'scripts/generate_mock_data.py',
            'scripts/data_ingestion.py',
            'scripts/data_cleaning.py',
            'scripts/feature_engineering.py'
        ]
        
        missing_files = []
        for file in required_files:
            if os.path.exists(file):
                self.log(f"✓ Found: {file}", "SUCCESS")
            else:
                self.log(f"✗ Missing: {file}", "ERROR")
                missing_files.append(file)
        
        if missing_files:
            self.log(f"Missing {len(missing_files)} required files!", "ERROR")
            return False
        
        self.log("Environment validation complete", "SUCCESS")
        return True
    
    def step_2_generate_data(self, skip=False):
        """Generate mock data if needed"""
        self.print_header("STEP 2: Generating Data")
        
        if skip:
            self.log("Skipping data generation (using existing data)", "WARNING")
            return True
        
        # Check if data already exists
        data_files = [
            f'{self.data_dir}/customers.csv',
            f'{self.data_dir}/tickets.json',
            f'{self.data_dir}/interactions.csv'
        ]
        
        existing = [f for f in data_files if os.path.exists(f)]
        
        if len(existing) == len(data_files):
            self.log(f"Data files already exist ({len(existing)}/{len(data_files)})", "INFO")
            regenerate = input("Regenerate data? (y/N): ").strip().lower()
            if regenerate != 'y':
                self.log("Using existing data files", "INFO")
                return True
        
        self.log("Generating mock data...", "INFO")
        
        try:
            import numpy as np
            import json
            
            # Run the generation
            os.makedirs(self.data_dir, exist_ok=True)
            
            # Generate customers
            num_customers = 200
            customer_ids = [f'CUST-{1000+i}' for i in range(num_customers)]
            customers = pd.DataFrame({
                'customer_id': customer_ids,
                'company_name': [f'Company {chr(65 + (i % 26))}{i}' for i in range(num_customers)],
                'industry': np.random.choice(['Tech', 'Retail', 'Finance', 'Healthcare', 'Manufacturing'], num_customers),
                'arr': np.random.randint(50000, 5000000, num_customers),
                'contract_type': np.random.choice(['Annual', 'Monthly'], num_customers),
                'renewal_date': '2026-12-31',
                'csm_name': np.random.choice(['Alice', 'Bob', 'Charlie'], num_customers)
            })
            customers.to_csv(f'{self.data_dir}/customers.csv', index=False)
            self.log(f"✓ Generated {len(customers)} customers", "SUCCESS")
            
            # Generate basic tickets and interactions
            import json
            tickets = [{'ticket_id': f'TKT-{2800+i}', 'customer_id': customer_ids[i % len(customer_ids)], 
                       'subject': 'Support Request', 'priority': 'Medium', 'status': 'Open',
                       'sentiment': 'Neutral', 'created_date': '2026-08-01T10:00:00', 'resolved_date': None}
                      for i in range(500)]
            with open(f'{self.data_dir}/tickets.json', 'w') as f:
                json.dump(tickets, f)
            self.log(f"✓ Generated {len(tickets)} tickets", "SUCCESS")
            
            interactions = pd.DataFrame({
                'interaction_id': [f'INT-{5000+i}' for i in range(1000)],
                'customer_id': [customer_ids[i % len(customer_ids)] for i in range(1000)],
                'interaction_type': ['Email'] * 1000,
                'description': ['Customer interaction'] * 1000,
                'timestamp': ['2026-08-01 10:00:00'] * 1000
            })
            interactions.to_csv(f'{self.data_dir}/interactions.csv', index=False)
            self.log(f"✓ Generated {len(interactions)} interactions", "SUCCESS")
            
            return True
            
        except Exception as e:
            self.log(f"Error generating data: {e}", "ERROR")
            return False
    
    def step_3_initialize_database(self):
        """Initialize database with schema"""
        self.print_header("STEP 3: Initializing Database")
        
        # Backup existing database
        if os.path.exists(self.db_path):
            backup_path = f"{self.db_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(self.db_path, backup_path)
            self.log(f"Backed up existing database to: {backup_path}", "WARNING")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Load and execute schema
            with open('database_schema.sql', 'r') as f:
                cursor.executescript(f.read())
            self.log("✓ Core schema created", "SUCCESS")
            
            # Load analytics schema
            with open('database_analytics.sql', 'r') as f:
                cursor.executescript(f.read())
            self.log("✓ Analytics schema created", "SUCCESS")
            
            # Load snapshot schema if exists
            if os.path.exists('database_snapshots.sql'):
                with open('database_snapshots.sql', 'r') as f:
                    cursor.executescript(f.read())
                self.log("✓ Snapshot schema created", "SUCCESS")
            
            conn.commit()
            conn.close()
            
            self.log("Database initialization complete", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Database initialization failed: {e}", "ERROR")
            return False
    
    def step_4_load_data(self):
        """Load CSV data into database"""
        self.print_header("STEP 4: Loading Data into Database")
        
        try:
            from scripts.data_ingestion import load_data as load_raw
            from scripts.data_cleaning import clean_data
            from scripts.feature_engineering import engineer_features
            
            self.log("Loading raw data from CSV/JSON...", "INFO")
            customers, tickets, interactions, churn_history = load_raw(self.data_dir)
            self.log(f"✓ Loaded {len(customers)} customers, {len(tickets)} tickets, {len(interactions)} interactions", "SUCCESS")
            
            self.log("Cleaning data...", "INFO")
            customers, tickets, interactions, churn_history = clean_data(customers, tickets, interactions, churn_history)
            self.log("✓ Data cleaned", "SUCCESS")
            
            self.log("Engineering features...", "INFO")
            customers, tickets = engineer_features(customers, tickets, interactions)
            self.log("✓ Features engineered (risk scores calculated)", "SUCCESS")
            
            # Load into database
            conn = sqlite3.connect(self.db_path)
            
            self.log("Inserting into database...", "INFO")
            customers.to_sql('customers', conn, if_exists='replace', index=False)
            tickets.to_sql('tickets', conn, if_exists='replace', index=False)
            interactions.to_sql('interactions', conn, if_exists='replace', index=False)
            
            conn.close()
            
            self.log(f"✓ Loaded {len(customers)} customers into database", "SUCCESS")
            self.log(f"✓ Loaded {len(tickets)} tickets into database", "SUCCESS")
            self.log(f"✓ Loaded {len(interactions)} interactions into database", "SUCCESS")
            
            return True
            
        except Exception as e:
            self.log(f"Data loading failed: {e}", "ERROR")
            import traceback
            self.log(traceback.format_exc(), "ERROR")
            return False
    
    def step_5_seed_analytics(self):
        """Seed analytics tables with historical data"""
        self.print_header("STEP 5: Seeding Analytics Data")
        
        if not os.path.exists('seed_analytics_data.py'):
            self.log("seed_analytics_data.py not found, skipping", "WARNING")
            return True
        
        try:
            import subprocess
            result = subprocess.run([sys.executable, 'seed_analytics_data.py'], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log("✓ Analytics data seeded successfully", "SUCCESS")
                return True
            else:
                self.log(f"Analytics seeding failed: {result.stderr}", "WARNING")
                return True  # Continue even if this fails
                
        except Exception as e:
            self.log(f"Analytics seeding error: {e}", "WARNING")
            return True  # Continue even if this fails
    
    def step_6_verify_database(self):
        """Verify database integrity"""
        self.print_header("STEP 6: Verifying Database")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check table counts
            cursor.execute("SELECT COUNT(*) FROM customers")
            customer_count = cursor.fetchone()[0]
            self.log(f"✓ Customers: {customer_count}", "SUCCESS")
            
            cursor.execute("SELECT COUNT(*) FROM tickets")
            ticket_count = cursor.fetchone()[0]
            self.log(f"✓ Tickets: {ticket_count}", "SUCCESS")
            
            cursor.execute("SELECT COUNT(*) FROM interactions")
            interaction_count = cursor.fetchone()[0]
            self.log(f"✓ Interactions: {interaction_count}", "SUCCESS")
            
            # Verify data quality
            cursor.execute("SELECT COUNT(*) FROM customers WHERE risk_score IS NOT NULL")
            risk_count = cursor.fetchone()[0]
            self.log(f"✓ Customers with risk scores: {risk_count}", "SUCCESS")
            
            conn.close()
            
            if customer_count == 0:
                self.log("No customers in database!", "ERROR")
                return False
            
            self.log("Database verification complete", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Verification failed: {e}", "ERROR")
            return False
    
    def step_7_create_snapshot(self):
        """Create initial data snapshot"""
        self.print_header("STEP 7: Creating Data Snapshot")
        
        try:
            if not os.path.exists('snapshot_manager.py'):
                self.log("snapshot_manager.py not found, skipping snapshot", "WARNING")
                return True
            
            from snapshot_manager import SnapshotManager
            
            manager = SnapshotManager(self.db_path)
            snapshot_name = f"Pipeline Run - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            snapshot_id = manager.create_snapshot(snapshot_name, "Automated Pipeline", 
                                                 "Automated data pipeline execution")
            
            if snapshot_id > 0:
                self.log(f"✓ Created snapshot ID: {snapshot_id}", "SUCCESS")
                return True
            else:
                self.log("Snapshot creation failed", "WARNING")
                return True  # Continue even if snapshot fails
                
        except Exception as e:
            self.log(f"Snapshot error: {e}", "WARNING")
            return True  # Continue even if snapshot fails
    
    def run_full_pipeline(self, skip_generate=False):
        """Run the complete data pipeline"""
        self.print_header("ChurnGuard AI - Automated Data Pipeline")
        self.log(f"Starting pipeline execution...", "INFO")
        self.log(f"Data directory: {self.data_dir}", "INFO")
        self.log(f"Database path: {self.db_path}", "INFO")
        
        steps = [
            ("Validate Environment", lambda: self.step_1_validate_environment()),
            ("Generate Data", lambda: self.step_2_generate_data(skip_generate)),
            ("Initialize Database", lambda: self.step_3_initialize_database()),
            ("Load Data", lambda: self.step_4_load_data()),
            ("Seed Analytics", lambda: self.step_5_seed_analytics()),
            ("Verify Database", lambda: self.step_6_verify_database()),
            ("Create Snapshot", lambda: self.step_7_create_snapshot())
        ]
        
        failed_steps = []
        
        for i, (name, func) in enumerate(steps, 1):
            self.log(f"\n{'='*70}", "INFO")
            self.log(f"Step {i}/{len(steps)}: {name}", "INFO")
            self.log(f"{'='*70}", "INFO")
            
            try:
                success = func()
                if not success:
                    failed_steps.append(name)
                    self.log(f"Step {i} FAILED: {name}", "ERROR")
                    
                    if name in ["Validate Environment", "Initialize Database", "Load Data"]:
                        self.log("Critical step failed, aborting pipeline", "ERROR")
                        break
            except Exception as e:
                failed_steps.append(name)
                self.log(f"Step {i} ERROR: {e}", "ERROR")
                
                if name in ["Validate Environment", "Initialize Database", "Load Data"]:
                    break
        
        # Final summary
        self.print_final_summary(failed_steps)
        
        return len(failed_steps) == 0
    
    def print_final_summary(self, failed_steps):
        """Print pipeline execution summary"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print("\n" + "=" * 70)
        print("  PIPELINE EXECUTION SUMMARY")
        print("=" * 70)
        
        if len(failed_steps) == 0:
            print("\n\033[92m✅ SUCCESS: All steps completed successfully!\033[0m")
        else:
            print(f"\n\033[91m❌ FAILED: {len(failed_steps)} step(s) failed:\033[0m")
            for step in failed_steps:
                print(f"  - {step}")
        
        print(f"\n⏱️  Total execution time: {duration:.2f} seconds")
        print(f"📊 Database: {self.db_path}")
        print(f"📁 Data directory: {self.data_dir}")
        
        # Show database stats
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM customers")
            customers = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tickets")
            tickets = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM interactions")
            interactions = cursor.fetchone()[0]
            conn.close()
            
            print(f"\n📈 Database contains:")
            print(f"   - {customers:,} customers")
            print(f"   - {tickets:,} tickets")
            print(f"   - {interactions:,} interactions")
        except:
            pass
        
        print("\n" + "=" * 70)
        
        if len(failed_steps) == 0:
            print("\n🚀 Next steps:")
            print("   1. Run the app: python -m streamlit run streamlit_app.py")
            print("   2. View at: http://localhost:8501")
            print("   3. Test SQL queries on Data Upload page")
        
        print("\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='ChurnGuard AI - Automated Data Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_pipeline.py                      # Run full pipeline
  python run_pipeline.py --data-dir mydata/   # Use custom data directory
  python run_pipeline.py --skip-generate      # Use existing data files
  python run_pipeline.py --verify-only        # Only verify database
        """
    )
    
    parser.add_argument('--data-dir', default='data', 
                       help='Data directory path (default: data)')
    parser.add_argument('--db-path', default='churnguard.db',
                       help='Database file path (default: churnguard.db)')
    parser.add_argument('--skip-generate', action='store_true',
                       help='Skip data generation, use existing files')
    parser.add_argument('--verify-only', action='store_true',
                       help='Only verify database, don\'t rebuild')
    
    args = parser.parse_args()
    
    pipeline = ChurnGuardPipeline(data_dir=args.data_dir, db_path=args.db_path)
    
    if args.verify_only:
        pipeline.step_6_verify_database()
    else:
        success = pipeline.run_full_pipeline(skip_generate=args.skip_generate)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
