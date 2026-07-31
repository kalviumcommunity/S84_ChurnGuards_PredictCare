# ChurnGuard AI - Quick Start Guide

## 🚀 Running the Application

### Option 1: Direct Run (Recommended)
```bash
streamlit run streamlit_app.py
```

### Option 2: Using Batch File (Windows)
```bash
run.bat
```

### Option 3: Using Shell Script (Mac/Linux)
```bash
chmod +x run.sh
./run.sh
```

## 📱 Application Pages

The application has **4 main pages** accessible from the sidebar:

### 1. **Executive Dashboard**
- Real-time KPIs: Churn Rate, Revenue at Risk, Average Risk Score, Retention ROI
- Churn Trend vs. Prevention Actions chart
- Risk Distribution by Segment
- Top Reasons for Dissatisfaction
- Recent High-Value Escalations table

### 2. **Risk Command Center**
- Health Score Summary (Low Risk, Medium, High Risk counts)
- Active Risk Alerts (Live Feed)
- High Risk Accounts table with risk scores and ARR
- Intervention actions

### 3. **Ticket Workspace**
- Search functionality for tickets and customers
- Detailed ticket view with conversation thread
- Customer 360 Context Panel showing:
  - Risk Score
  - ARR (Annual Recurring Revenue)
  - Sentiment Analysis
  - Active Escalations
  - AI Recommendations
  - Recent Interactions timeline

### 4. **Customer Directory**
- Comprehensive customer profile
- Company information and stakeholder details
- Health Metrics (CSAT Score, Usage, Open Tickets)
- Interaction Timeline
- Retention Strategy with AI recommendations
- Account Team members

## 🎨 Design Features

✅ **Light Theme** - Clean white background matching enterprise analytics
✅ **Inter Font** - Professional typography
✅ **Color-Coded Risk Levels**:
  - 🔴 Critical (Red)
  - 🟠 High (Orange)
  - 🟡 Medium (Yellow)
  - 🔵 Low (Blue)

✅ **Responsive Layout** - Adapts to different screen sizes
✅ **Interactive Charts** - Plotly visualizations
✅ **Real-time Data** - Generated sample data for demonstration

## 🔧 Configuration

The app runs on: **http://localhost:8501**

To change the port:
```bash
streamlit run streamlit_app.py --server.port 8080
```

## 📊 Data

Currently using **generated sample data**. To connect real data:
1. Replace the `load_data()` function in `streamlit_app.py`
2. Connect to your CSV files or database
3. Update the data structure as needed

## 🤝 Team Collaboration

This project is ready for team collaboration:
- ✅ Git repository initialized
- ✅ `.gitignore` configured
- ✅ `requirements.txt` updated
- ✅ Documentation complete

## 📝 Next Steps

1. **Run the app**: `streamlit run streamlit_app.py`
2. **Test all 4 pages** using the sidebar navigation
3. **Customize** data sources and styling as needed
4. **Push to Git** repository for team access

## ❓ Need Help?

- Check `README.md` for detailed documentation
- See `CONTRIBUTING.md` for development guidelines
- Review the code comments in `streamlit_app.py`

---

**Version:** 2.0  
**Last Updated:** July 31, 2026  
**Team:** Akshit Sharma, Arman Singh, Saksham Kaushal
