# ChurnGuard AI - Database Documentation

## Overview
This database stores customer churn prediction data including customer information, support tickets, interactions, usage metrics, and risk alerts.

## Database Type
**SQLite** - Lightweight, serverless database (file: `churnguard.db`)

## Setup Instructions

### 1. Initialize Database
Run the initialization script to create the database and load sample data:

```bash
python init_database.py
```

This will:
- Create `churnguard.db` SQLite database file
- Execute the schema from `database_schema.sql`
- Load sample data for testing

### 2. Verify Database
After initialization, you should see:
- 6 tables created
- 3 views created
- Sample data across all tables

## Database Schema

### Tables

#### 1. **customers**
Stores customer account information and churn risk metrics.

**Key Columns:**
- `customer_id` (PK): Unique customer identifier
- `company_name`: Customer company name
- `risk_score`: Churn risk score (0-100)
- `health_status`: Low Risk | Medium | Critical
- `arr`: Annual Recurring Revenue
- `sentiment`: Positive | Neutral | Negative
- `renewal_date`: Next renewal date

**Use Cases:**
- Track customer health and risk
- Monitor ARR and revenue metrics
- Identify high-risk accounts

---

#### 2. **tickets**
Stores support ticket information.

**Key Columns:**
- `ticket_id` (PK): Unique ticket identifier (e.g., TKT-2842)
- `customer_id` (FK): Links to customers table
- `subject`: Ticket subject/title
- `priority`: Low | Medium | High | Critical
- `status`: Open | In Progress | Awaiting Response | Resolved | Closed
- `sentiment`: Ticket sentiment analysis

**Use Cases:**
- Track support issues by customer
- Monitor ticket resolution times
- Identify patterns in critical tickets

---

#### 3. **interactions**
Stores customer interaction history (calls, emails, meetings).

**Key Columns:**
- `interaction_id` (PK): Unique interaction identifier
- `customer_id` (FK): Links to customers table
- `interaction_type`: Call | Email | Meeting | QBR | Training | Survey
- `interaction_date`: When interaction occurred
- `sentiment`: Interaction sentiment
- `notes`: Interaction notes/summary

**Use Cases:**
- Track customer engagement frequency
- Analyze sentiment trends
- Monitor last contact dates

---

#### 4. **usage_metrics**
Stores product usage metrics by customer and date.

**Key Columns:**
- `metric_id` (PK): Unique metric record
- `customer_id` (FK): Links to customers table
- `metric_date`: Date of metrics
- `active_users`: Number of active users that day
- `feature_usage_score`: Feature adoption score (0-100)
- `api_calls`: Number of API calls

**Use Cases:**
- Monitor product adoption
- Detect usage drops
- Track feature engagement

---

#### 5. **risk_alerts**
Stores automated risk alerts for customers.

**Key Columns:**
- `alert_id` (PK): Unique alert identifier
- `customer_id` (FK): Links to customers table
- `alert_type`: Type of risk detected
- `severity`: Low | Medium | High | Critical
- `message`: Alert description
- `is_resolved`: Alert resolution status

**Use Cases:**
- Monitor active risk alerts
- Track alert resolution
- Prioritize intervention actions

---

#### 6. **stakeholders**
Stores key stakeholder information per customer.

**Key Columns:**
- `stakeholder_id` (PK): Unique stakeholder identifier
- `customer_id` (FK): Links to customers table
- `name`: Stakeholder name
- `role`: Job title
- `influence_level`: Low | Medium | High | Champion
- `is_active`: Whether stakeholder is still active

**Use Cases:**
- Track key contacts per account
- Monitor stakeholder changes
- Identify champions vs. detractors

---

### Views

#### 1. **vw_high_risk_customers**
Pre-aggregated view of high-risk customers with open ticket counts.

**Use Case:** Quick dashboard for at-risk accounts

---

#### 2. **vw_customer_engagement**
Summary of customer interaction frequency and sentiment.

**Use Case:** Monitor engagement levels

---

#### 3. **vw_weekly_usage_trends**
Weekly aggregation of usage metrics.

**Use Case:** Trend analysis and anomaly detection

---

## Sample Queries

### Get high-risk customers with details
```sql
SELECT * FROM vw_high_risk_customers
WHERE risk_score > 75
ORDER BY arr DESC;
```

### Find customers with critical open tickets
```sql
SELECT c.company_name, c.risk_score, t.subject, t.created_at
FROM customers c
JOIN tickets t ON c.customer_id = t.customer_id
WHERE t.priority = 'Critical' AND t.status = 'Open'
ORDER BY c.risk_score DESC;
```

### Check recent risk alerts
```sql
SELECT c.company_name, ra.alert_type, ra.severity, ra.message, ra.created_at
FROM risk_alerts ra
JOIN customers c ON ra.customer_id = c.customer_id
WHERE ra.is_resolved = FALSE
ORDER BY ra.created_at DESC;
```

### Monitor usage trends
```sql
SELECT * FROM vw_weekly_usage_trends
WHERE customer_id = 1
ORDER BY week DESC
LIMIT 10;
```

---

## Integration with Streamlit App

The database can be integrated into the Streamlit app for:
- **Real data loading** instead of mock data
- **Historical trend analysis**
- **Alert monitoring dashboards**
- **Customer 360 views**

### Example Python Integration
```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('churnguard.db')

# Load high-risk customers
df = pd.read_sql_query("SELECT * FROM vw_high_risk_customers", conn)

# Display in Streamlit
st.dataframe(df)

conn.close()
```

---

## Maintenance

### Backup Database
```bash
# Copy the database file
cp churnguard.db churnguard_backup_YYYYMMDD.db
```

### Reset Database
```bash
# Re-run initialization script
python init_database.py
```

### Add More Sample Data
Edit `init_database.py` and add records to the `seed_sample_data()` function.

---

## Future Enhancements

- [ ] Add automated alert triggers
- [ ] Implement time-series forecasting tables
- [ ] Add audit log table for changes
- [ ] Create materialized aggregation tables
- [ ] Add customer journey mapping tables

---

## Files

- `database_schema.sql` - Database schema definition
- `init_database.py` - Database initialization script
- `churnguard.db` - SQLite database file (generated)
- `DATABASE_README.md` - This documentation

---

**Created:** August 2026  
**Version:** 1.0  
**Purpose:** First PR - Basic database schema for ChurnGuard AI
