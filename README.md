# Customer Support Churn Prevention System - Streamlit Version

A data-driven platform built with **Python and Streamlit** combining support tickets, CRM, billing, and cancellation history to predict customer churn, generate proactive alerts, and provide actionable retention recommendations.
The dashboard is intended for local customer-risk exploration and retention planning.

## Tech Stack (Sprint 1 Curriculum)

This project uses technologies from the **Turn Data Into a Product** curriculum:

- **Python 3.10+** - Core programming language
- **Pandas** - Data cleaning, transformation, and analysis
- **NumPy** - Numerical computation and vectorized processing
- **Streamlit** - Interactive dashboard and data product interfaces
- **Plotly** - Interactive visualizations and charts
- **SQL** (Future) - Business analytics and database queries

## Project Structure

```
churn-prevention-system/
├── streamlit_app.py          # Main Streamlit application (Routing & Auth)
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── QUICKSTART.md            # Quick start guide
├── .env.example             # Environment variables template
├── data/                    # CSV/JSON datasets (to be added)
├── pages/                   # Modular Page Components
│   ├── 1_dashboard.py       # Executive Dashboard
│   ├── 2_risk_center.py     # Risk Command Center
│   ├── 3_tickets.py         # Ticket Workspace
│   ├── 4_directory.py       # Customer Directory & 360 View
│   └── 5_data_upload.py     # Data Upload & Validation
├── scripts/                 # Data processing scripts
│   ├── data_ingestion.py    # CSV & JSON data loading
│   ├── data_cleaning.py     # Missing values, duplicates, standardization
│   ├── feature_engineering.py # Derived business columns
│   └── churn_analysis.py    # GroupBy, KPIs, behavioral analysis
├── utils/                   # Shared Utilities
│   ├── data_loader.py       # DB connections & CSS injection
│   └── validators.py        # Schema validation engine
└── tests/                   # Automated Test Suite
    ├── test_etl_pipeline.py # End-to-End ETL tests
    └── test_upload_validation.py # Schema validation tests
```

## Installation

### 1. Set up Python virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run streamlit_app.py
```

The application will open automatically at **http://localhost:8501**

## Features Implemented

### 📊 Executive Dashboard
- **KPI Cards** - Projected churn rate, revenue at risk, prevention actions
- **Churn Trends** - Stacked bar charts showing actual vs prevented churn
- **Segment Analysis** - Pie chart of risk distribution
- **Dissatisfaction Analysis** - Top reasons with progress bars

### 🚨 Risk Command Center
- **Health Score Summary** - Low Risk, Medium, Critical counts
- **Active Risk Alerts** - Real-time feed of critical events
- **High-Risk Accounts Table** - Sortable list with risk scores
- **Account Details** - ARR, last activity, risk indicators

### 🎫 Support Workspace
- **Ticket Management** - Search, filter, and prioritize tickets
- **Customer 360 Context** - Risk scores and sentiment per ticket
- **Priority Indicators** - Visual badges for Critical, High, Medium, Low
- **Quick Metrics** - Open tickets, response time, high-risk count

### 👤 Customer 360 Profile
- **Account Overview** - Industry, ARR, contract details
- **Key Metrics** - Health score, support tickets, login activity
- **Customer Timeline** - Chronological interaction history
- **AI Recommendations** - Retention strategies and actions

## Sprint 1 Skills Demonstrated

### Data Handling (Modules 2.3-2.6)
- ✅ Pandas DataFrame operations
- ✅ Data cleaning and transformation workflows
- ✅ NumPy vectorized computations
- ✅ Dataset profiling and quality assessment

### Analysis & Insights (Modules 2.29-2.36)
- ✅ GroupBy aggregation and segment insights
- ✅ KPI definition and business metric design
- ✅ Behavioral analysis and user segmentation
- ✅ Anomaly detection and risk identification

### Visualization & Reporting (Modules 2.45-2.50)
- ✅ Interactive Plotly chart design
- ✅ KPI card and summary metric display
- ✅ Data storytelling and insight narrative
- ✅ Executive reporting and stakeholder communication

### Streamlit Development (Modules 2.51-2.57)
- ✅ App structure and navigation
- ✅ Interactive filters and widgets
- ✅ Session state management
- ✅ Real-time KPI dashboard development
- ✅ Alert monitoring and threshold detection

## Data Sources

### Expected CSV/JSON Files (to be added in `data/` folder)

1. **customers.csv** - Customer account information
   - customer_id, company_name, industry, arr, contract_type, renewal_date, csm_name

2. **tickets.csv** - Support ticket records
   - ticket_id, customer_id, subject, priority, status, created_date, resolved_date, sentiment

3. **interactions.csv** - Customer interaction timeline
   - interaction_id, customer_id, interaction_type, description, timestamp

4. **churn_history.csv** - Historical churn events
   - customer_id, churn_date, churn_reason, revenue_lost

### Data Ingestion Workflow (Module 2.15)

```python
import pandas as pd

# CSV loading with proper encoding
customers = pd.read_csv('data/customers.csv', encoding='utf-8')

# JSON loading for nested data
tickets = pd.read_json('data/tickets.json')

# Basic ingestion checks
print(f"Customers loaded: {len(customers)} rows")
print(f"Tickets loaded: {len(tickets)} rows")
```

## Development Workflow (Modules 2.11-2.13)

### Setup Commands

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Freeze current dependencies
pip freeze > requirements.txt
```

### Git Workflow (Module 2.12)

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit: Streamlit churn prevention dashboard"

# Create feature branch
git checkout -b feature/customer-profile

# Push to GitHub
git remote add origin <your-repo-url>
git push -u origin main
```

## Future Enhancements

### Phase 2: SQL Integration (Modules 2.37-2.44)
- [ ] Connect to SQL database for persistent storage
- [ ] SQL business metrics query design
- [ ] Window functions for ranking and trends
- [ ] Query optimization and views

### Phase 3: Automation (Modules 2.58-2.60)
- [ ] Automated data pipeline execution
- [ ] GitHub Actions for validation
- [ ] Scheduled report generation
- [ ] Email alert integration

### Phase 4: Advanced Analytics
- [ ] Machine learning churn prediction model
- [ ] Real-time risk score calculation
- [ ] Anomaly detection algorithms
- [ ] Customer lifetime value (CLV) forecasting

## Team

- **Akshit Sharma**
- **Arman Singh**
- **Saksham Kaushal**

**Version:** 1.1  
**Date:** July 30, 2026

## Documentation

For detailed curriculum alignment, see:
- **Module 2.51-2.57** - Streamlit foundations and dashboard development
- **Module 2.3-2.6** - Python data structures and Pandas workflows
- **Module 2.29-2.36** - Business analytics and KPI analysis
- **Module 2.45-2.50** - Visualization and executive reporting

---

Built with Python, Streamlit, and Pandas for enterprise-scale customer retention.
