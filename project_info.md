# ChurnGuard AI - Technical Documentation

## 🎯 Project Overview
Customer churn prevention system with SQLite database backend, automated ETL pipeline, and interactive Streamlit dashboard for predicting and preventing customer churn.

---

## 🚀 Quick Start (One Command)

```bash
# Setup entire system (13 seconds)
python run_pipeline.py

# Run application
python -m streamlit run streamlit_app.py
```

**URL:** http://localhost:8501

---

## 📊 Database Architecture

### **Database Type:** SQLite (`churnguard.db`)

### **Core Tables (6)**
1. **customers** - Customer accounts, risk scores, health status, ARR
2. **tickets** - Support tickets with priority and sentiment
3. **interactions** - Customer activity logs (calls, emails, meetings)
4. **usage_metrics** - Product usage data
5. **risk_alerts** - Automated churn risk alerts
6. **stakeholders** - Key contacts per customer

### **Analytics Tables (9)**
- `churn_predictions` - ML predictions
- `customer_health_history` - Historical health snapshots
- `intervention_actions` - CSM interventions
- `nps_surveys` - Net Promoter Score data
- `revenue_events` - Upsell/downsell/churn events
- `feature_adoption` - Product feature usage
- `contracts` - Contract details
- `risk_score_history` - Risk score changes
- `customer_health_summary` - Daily health summaries

### **Database Views (3)**
- `vw_high_risk_customers` - At-risk accounts
- `vw_customer_engagement` - Interaction frequency
- `vw_weekly_usage_trends` - Weekly usage patterns

### **Current Data**
- 200 customers
- 500 tickets
- 1,000 interactions
- 28,835 total records

---

## 🔄 Automated Data Pipeline (Module 2.58)

### **Command**
```bash
python run_pipeline.py
```

### **7 Automated Steps**

1. **Validate Environment** - Check files exist
2. **Generate Data** - Create mock data (or use existing)
3. **Initialize Database** - Create schema + backup old DB
4. **Load Data** - ETL pipeline (Extract, Transform, Load)
5. **Seed Analytics** - Populate analytics tables
6. **Verify Database** - Check integrity
7. **Create Snapshot** - Version control

### **Features**
- ✅ Single command execution
- ✅ Color-coded logging (green/red/yellow)
- ✅ Automatic backups before rebuild
- ✅ 13-second execution time
- ✅ Command-line arguments support

### **Arguments**
```bash
--data-dir       # Custom data directory (default: data)
--db-path        # Custom database file (default: churnguard.db)
--skip-generate  # Use existing data files
--verify-only    # Only verify, don't rebuild
```

### **Pipeline Architecture**
```
run_pipeline.py → Validate → Generate → Init DB → ETL → 
Seed Analytics → Verify → Snapshot
```

---

## 🔍 SQL Query Integration (Module 2.38-2.40)

### **Query Functions in db_queries.py**

1. **get_dashboard_kpis()** - Aggregated metrics (AVG, SUM, COUNT)
2. **get_high_risk_customers(threshold)** - Filter by risk score
3. **get_open_tickets(priority)** - Ticket queue management
4. **get_revenue_at_risk()** - Financial impact calculation
5. **get_ticket_metrics()** - Support analytics
6. **search_customers(term)** - Customer lookup (LIKE queries)
7. **get_renewal_pipeline(days)** - Upcoming renewals

### **SQL Techniques Used**
- Aggregations: SUM, AVG, COUNT, GROUP BY
- Filtering: WHERE, HAVING
- Joins: LEFT JOIN for customer-ticket relationships
- Conditional logic: CASE WHEN statements
- Date filtering: Renewal date queries

### **Testing**
- ✅ All 8 unit tests passing (`test_sql_integration.py`)
- ✅ Interactive SQL demo on Data Upload page

---

## 📁 Project Structure

```
S84_ChurnGuards_PredictCare/
│
├── streamlit_app.py           # 5-page web application
├── run_pipeline.py            # Automated orchestrator
├── db_queries.py              # SQL query functions
├── churnguard.db              # SQLite database (4.19 MB)
│
├── database_schema.sql        # Core schema
├── database_analytics.sql     # Analytics schema
├── database_snapshots.sql     # Version history
│
├── init_database.py           # Database initialization
├── load_csv_to_db.py          # CSV to DB loader
├── seed_analytics_data.py     # Populate analytics
├── snapshot_manager.py        # Version management
│
├── scripts/
│   ├── generate_mock_data.py  # Create sample data
│   ├── data_ingestion.py      # Load CSV/JSON
│   ├── data_cleaning.py       # Clean data
│   └── feature_engineering.py # Calculate features
│
├── data/
│   ├── customers.csv          # 200 customers
│   ├── tickets.json           # 500 tickets
│   └── interactions.csv       # 1,000 interactions
│
├── test_sql_integration.py    # SQL tests
├── verify_database.py         # DB validation
│
├── README.md                  # Project overview
├── QUICKSTART.md              # Setup guide
└── project_info.md            # This file
```

---

## 💻 Application Features

### **Page 1: Executive Dashboard**
- KPI cards (churn rate, revenue at risk)
- Risk distribution pie chart
- Monthly churn trends
- Dynamic risk filters
- CSV export

### **Page 2: Risk Command Center**
- Health score summary
- Active alerts panel
- High-risk accounts table
- Alert management

### **Page 3: Ticket Workspace**
- Ticket queue with search
- Priority badges
- Customer context
- Sentiment analysis

### **Page 4: Customer Directory**
- Search by name/ID
- Risk filtering
- Customer 360 view
- Interaction timeline
- CSV export

### **Page 5: Data Upload**
- Browser-based CSV/JSON upload
- Data preview
- One-click database insertion
- Current database status
- Interactive SQL demo

---

## 🔧 Sample Queries

### **High-Risk Customers**
```sql
SELECT * FROM vw_high_risk_customers
WHERE risk_score >= 70
ORDER BY arr DESC
```

### **Revenue at Risk**
```sql
SELECT 
    health_status,
    SUM(arr) as total_arr,
    COUNT(*) as customer_count
FROM customers
WHERE health_status IN ('Critical', 'Medium')
GROUP BY health_status
```

### **Open Critical Tickets**
```sql
SELECT c.company_name, t.subject, t.created_at
FROM tickets t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.priority = 'Critical' AND t.status = 'Open'
ORDER BY c.risk_score DESC
```

---

## ⚙️ Setup Instructions

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run Automated Pipeline**
```bash
python run_pipeline.py
```
This creates database, loads data, and verifies everything.

### **3. Launch Application**
```bash
python -m streamlit run streamlit_app.py
```

### **4. Access Dashboard**
Open browser to: http://localhost:8501

---

## 🧪 Testing & Validation

### **Run Tests**
```bash
# SQL integration tests
python test_sql_integration.py

# Database verification
python run_pipeline.py --verify-only

# Database integrity
python verify_database.py
```

### **Expected Results**
- ✅ 8/8 SQL tests passing
- ✅ 200 customers with risk scores
- ✅ 500 tickets loaded
- ✅ 1,000 interactions recorded

---

## 🔧 Troubleshooting

### **Issue: "No data to display"**
**Solution:** Run `python run_pipeline.py`

### **Issue: Database locked**
**Solution:** Close Streamlit app, then run pipeline

### **Issue: Import errors**
**Solution:** `pip install -r requirements.txt`

### **Issue: KeyError in app**
**Solution:** Regenerate database with `python init_database.py`

---

## 📊 Database Maintenance

### **Backup Database**
```bash
copy churnguard.db churnguard_backup.db
```

### **Reset Database**
```bash
python run_pipeline.py
```

### **Verify Integrity**
```bash
python run_pipeline.py --verify-only
```

---

## 🎯 Key Technologies

**Backend:**
- Python 3.12
- SQLite 3
- Pandas 2.x
- NumPy 1.26

**Frontend:**
- Streamlit 1.40
- Plotly 5.24
- Custom CSS

**Data Pipeline:**
- ETL scripts (ingestion, cleaning, feature engineering)
- Automated orchestrator
- Version control with snapshots

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Database Size | 4.19 MB |
| Total Records | 28,835 |
| Pipeline Execution | 13 seconds |
| Page Load Time | < 2 seconds |
| Test Coverage | 100% (8/8) |

---

## ✅ Completed Milestones

**Sprint 1 (Data & Analytics):**
- [x] **Module 2.36** - Real risk calculation (5 factors: tickets, activity, sentiment, renewal, CSAT)
- [x] **Module 2.37** - Database schema & population
- [x] **Module 2.38-2.40** - SQL query integration (7 functions)
- [x] **Module 2.52** - Browser-based data upload
- [x] **Module 2.58** - Automated data pipeline
- [x] **Module 2.60** - Complete documentation

**Sprint 2 Prep (AI/RAG Foundation):**
- [x] **Module 3.10** - Development environment setup (venv, .env, .gitignore)
- [x] **Module 3.11** - GitHub workflow setup (branches, PRs, templates)

**Next Up:** Module 3.12 - LLM API Access 🚀

---

## 🎯 Risk Calculation Algorithm (Module 2.36)

### **Real-Time Risk Scoring**
Customers are scored 0-100 based on weighted business factors:

**Risk Components:**
1. **Open Tickets (0-25 pts)** - Critical tickets +5pts each, all open tickets +2pts
2. **Last Activity (0-20 pts)** - Days since login: 30+=20pts, 14-30=15pts, 7-14=10pts
3. **Sentiment (0-25 pts)** - Negative=25pts, Neutral=10pts, Positive=0pts
4. **Renewal Date (0-20 pts)** - Past due=20pts, <30 days=15pts, <60 days=10pts
5. **CSAT Score (0-10 pts)** - Score ≤2.0=10pts, ≤3.0=7pts, ≤4.0=3pts

**Health Status:**
- **Critical:** Risk ≥70
- **Medium:** Risk 50-69
- **Low Risk:** Risk <50

**Implementation:** `calculate_real_risk_score()` in streamlit_app.py

---

## 🚀 Production Deployment

### **Pre-Deployment Checklist**
- [x] All tests passing
- [x] Database schema finalized
- [x] Documentation complete
- [x] Error handling implemented
- [x] Automated setup working

### **Deployment Steps**
1. Clone repository
2. `pip install -r requirements.txt`
3. `python run_pipeline.py`
4. `streamlit run streamlit_app.py`

---

## 👥 Team
- Akshit Sharma
- Arman Singh
- Saksham Kaushal

**Version:** 1.0  
**Status:** ✅ Production Ready  
**Last Updated:** August 12, 2026
