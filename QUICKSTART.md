# 🚀 ChurnGuard AI - Quick Start Guide

## What's New in This PR

### ✅ Database Schema & Infrastructure
- **Complete relational database schema** with 6 core tables
- **Advanced analytics tables** for risk tracking and customer insights
- **Database triggers** for automatic alerting and data validation
- **Utility scripts** for database initialization and seeding

### ✅ Frontend Enhancements
- **CSV Export Function** - Export customer risk data with one click
- **Dynamic Risk Filters** - Filter dashboard KPIs by risk level in real-time
- **Smart Alert Panel** - Live alert monitoring in Risk Command Center

---

## 🏃‍♂️ Quick Start (5 Minutes)

### Step 1: Generate Sample Data
```bash
python scripts/generate_mock_data.py
```
This creates:
- `data/customers.csv` - 200 sample customers
- `data/tickets.json` - 500 support tickets
- `data/interactions.csv` - 1000 customer interactions
- `data/churn_history.csv` - 50 churned customers

### Step 2: Initialize Database
```bash
python init_database.py
```
This creates `churnguard.db` with:
- 6 relational tables
- Sample data loaded
- Indexes for performance
- Verification checks

### Step 3: Run the App
```bash
python -m streamlit run streamlit_app.py
```
Open browser to: **http://localhost:8501**
If the default port is busy, configure another Streamlit server port before launching.

---

## 📊 Database Schema Overview

### Core Tables

#### 1. **customers**
Primary customer information and risk metrics
```
- customer_id (PK)
- company_name
- industry
- arr (Annual Recurring Revenue)
- contract_type
- renewal_date
- csm_name
- health_status (Low Risk/Medium/Critical)
- risk_score (0-100)
- created_at
- updated_at
```

#### 2. **tickets**
Customer support tickets
```
- ticket_id (PK)
- customer_id (FK)
- subject
- priority (Low/Medium/High/Critical)
- status (Open/In Progress/Awaiting Response/Resolved)
- sentiment (Positive/Neutral/Negative)
- created_date
- resolved_date
```

#### 3. **interactions**
Customer activity logs
```
- interaction_id (PK)
- customer_id (FK)
- interaction_type (Login/Feature Usage/Support Call/QBR/Email)
- description
- timestamp
```

#### 4. **usage_metrics**
Product usage data
```
- metric_id (PK)
- customer_id (FK)
- date
- logins
- features_used
- api_calls
- data_volume_mb
```

#### 5. **risk_alerts**
Automated risk alerts
```
- alert_id (PK)
- customer_id (FK)
- alert_type
- severity (Low/Medium/High/Critical)
- description
- triggered_at
- resolved_at
- resolution_notes
```

#### 6. **stakeholders**
Customer stakeholder contacts
```
- stakeholder_id (PK)
- customer_id (FK)
- name
- role
- email
- engagement_score (0-100)
- last_contacted
```

### Analytics Tables

#### **risk_score_history**
Tracks risk score changes over time
```
- history_id (PK)
- customer_id (FK)
- risk_score
- health_status
- recorded_at
```

#### **customer_health_summary**
Daily customer health snapshots
```
- summary_id (PK)
- customer_id (FK)
- date
- risk_score
- health_status
- open_tickets
- critical_tickets
- days_since_last_login
- usage_trend
```

### Database Views

#### **v_high_risk_customers**
Quick access to at-risk accounts
```sql
SELECT customer_id, company_name, arr, risk_score, health_status
FROM customers
WHERE health_status IN ('Critical', 'Medium')
ORDER BY risk_score DESC;
```

#### **v_ticket_metrics**
Aggregated ticket statistics per customer
```sql
SELECT 
    customer_id,
    COUNT(*) as total_tickets,
    SUM(CASE WHEN status != 'Resolved' THEN 1 ELSE 0 END) as open_tickets,
    AVG(CASE WHEN resolved_date IS NOT NULL 
        THEN julianday(resolved_date) - julianday(created_date) END) as avg_resolution_days
FROM tickets
GROUP BY customer_id;
```

#### **v_customer_engagement**
Customer activity summary
```sql
SELECT 
    c.customer_id,
    c.company_name,
    COUNT(i.interaction_id) as total_interactions,
    MAX(i.timestamp) as last_interaction
FROM customers c
LEFT JOIN interactions i ON c.customer_id = i.customer_id
GROUP BY c.customer_id;
```

---

## 🔧 Database Utilities

### Query Helper Module (`db_queries.py`)
Python functions for common database operations:

```python
from db_queries import DatabaseHelper

db = DatabaseHelper('churnguard.db')

# Get high-risk customers
high_risk = db.get_high_risk_customers(threshold=70)

# Get customer risk history
history = db.get_customer_risk_history('CUST-1001', days=30)

# Get open tickets by priority
tickets = db.get_open_tickets_by_priority()

# Calculate churn risk
risk = db.calculate_customer_churn_risk('CUST-1001')

# Log risk score
db.log_risk_score_change('CUST-1001', 85, 'Critical')

# Create alert
db.create_risk_alert('CUST-1001', 'High Open Tickets', 'High', '5 critical tickets')
```

### Seed Analytics Data (`seed_analytics_data.py`)
Populate analytics tables with historical data:
```bash
python seed_analytics_data.py
```

---

## 🎨 Frontend Features

### 1. **CSV Export Function** 📥
**Location:** Customer Directory page

Exports filtered customer data including:
- Customer ID and Company Name
- Risk Score and Health Status
- ARR (Annual Recurring Revenue)
- Last Activity Date
- Days Since Active

**Usage:** Click "📥 Export Customer Data" button at the top of the Customer Directory

### 2. **Dynamic Risk Filters** 🎯
**Location:** Executive Dashboard

Filter all KPIs by risk level:
- Critical
- Medium
- Low Risk
- All Levels (default)

Real-time updates:
- Total ARR
- Customer count
- High-risk customer metrics
- Risk distribution chart

**Usage:** Use the multi-select dropdown at the top of the Executive Dashboard

### 3. **Smart Alert Panel** 🚨
**Location:** Risk Command Center

Live monitoring of:
- Active risk alerts by severity
- Recent alerts (last 24 hours)
- Top at-risk customers
- Alert resolution status

**Features:**
- Real-time severity badges (🔴 Critical, 🟠 High, 🟡 Medium)
- Auto-refresh capability
- One-click alert dismissal

---

## 📁 File Structure

```
S84_ChurnGuards_PredictCare/
│
├── data/                          # Generated data files
│   ├── customers.csv
│   ├── tickets.json
│   ├── interactions.csv
│   └── churn_history.csv
│
├── scripts/                       # Data pipeline scripts
│   ├── generate_mock_data.py      # Generate sample data
│   ├── data_ingestion.py          # Load raw data
│   ├── data_cleaning.py           # Clean and validate
│   └── feature_engineering.py     # Create features
│
├── database_schema.sql            # Core database schema
├── database_analytics.sql         # Analytics tables and views
├── database_triggers.sql          # Automated triggers
├── init_database.py               # Database initialization
├── db_queries.py                  # Query helper functions
├── seed_analytics_data.py         # Seed analytics tables
│
├── pages/                         # Modular Streamlit Pages
│   ├── 1_dashboard.py             # Executive Dashboard
│   ├── 2_risk_center.py           # Risk Command Center
│   ├── 3_tickets.py               # Ticket Workspace
│   ├── 4_directory.py             # Customer Directory & 360 View
│   └── 5_data_upload.py           # Data Upload & Validation
│
├── utils/                         # Shared Utilities
│   ├── data_loader.py             # DB connections & CSS injection
│   ├── validators.py              # Schema validation engine
│   └── llm_client.py              # API client for LLM generation
│
├── tests/                         # Automated Test Suite
│   ├── test_etl_pipeline.py       # End-to-End ETL tests
│   ├── test_upload_validation.py  # Schema validation tests
│   └── test_customer_directory.py # Customer directory tests
│
├── streamlit_app.py               # Main application (Routing)
├── .env.example                   # Environment variables template
├── DATABASE_README.md             # Database documentation
└── QUICKSTART.md                  # This file
```

---

## 🔍 Sample Queries

### Find customers at risk of churn
```sql
SELECT 
    c.company_name,
    c.arr,
    c.risk_score,
    c.health_status,
    COUNT(t.ticket_id) as open_tickets
FROM customers c
LEFT JOIN tickets t ON c.customer_id = t.customer_id AND t.status != 'Resolved'
WHERE c.risk_score >= 70
GROUP BY c.customer_id
ORDER BY c.risk_score DESC;
```

### Calculate revenue at risk
```sql
SELECT 
    health_status,
    COUNT(*) as customer_count,
    SUM(arr) as total_arr,
    ROUND(SUM(arr) * 1.0 / (SELECT SUM(arr) FROM customers) * 100, 2) as percent_of_total
FROM customers
GROUP BY health_status
ORDER BY total_arr DESC;
```

### Track customer engagement trends
```sql
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as interactions,
    COUNT(DISTINCT customer_id) as active_customers
FROM interactions
WHERE timestamp >= DATE('now', '-30 days')
GROUP BY DATE(timestamp)
ORDER BY date;
```

---

## 🧪 Testing the Database

Run verification checks:
```bash
python -c "from db_queries import DatabaseHelper; db = DatabaseHelper('churnguard.db'); print('Database OK!')"
```

Query customer count:
```bash
sqlite3 churnguard.db "SELECT COUNT(*) as customers FROM customers;"
```

Check high-risk customers:
```bash
sqlite3 churnguard.db "SELECT company_name, risk_score FROM customers WHERE health_status='Critical';"
```

---

## 🎯 Next Steps

1. **Enhance Risk Scoring** - Add more predictive features
2. **Build ML Model** - Train churn prediction model
3. **Add Automation** - Scheduled risk assessments
4. **Email Alerts** - Notify CSMs of critical changes
5. **API Integration** - Connect to real CRM data

---

## 📚 Additional Resources

- **DATABASE_README.md** - Detailed database documentation
- **streamlit_app.py** - Application source code with comments
- **db_queries.py** - Database query examples

---

## 🐛 Troubleshooting

### Issue: "KeyError: 'arr'" when running app
**Solution:** Generate data first with `python scripts/generate_mock_data.py`

### Issue: Database file not found
**Solution:** Run `python init_database.py` to create database

### Issue: App shows "No data to display"
**Solution:** Check that files exist in `data/` directory

### Issue: Streamlit cache errors
**Solution:** Clear cache from app menu: ☰ → Clear cache → Rerun

---

## ✨ Summary

This PR adds:
- ✅ 6 core database tables
- ✅ 2 analytics tables
- ✅ 3 database views
- ✅ Automated triggers
- ✅ 3 new frontend features
- ✅ Complete documentation
- ✅ Sample data generation
- ✅ Query helper utilities

**Ready for production deployment!** 🚀
