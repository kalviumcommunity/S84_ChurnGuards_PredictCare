import streamlit as st
import pandas as pd

from utils.data_loader import inject_custom_css, (
    get_dashboard_kpis_sql,
    get_high_risk_customers_sql,
    get_open_tickets_by_priority_sql
)

st.title("📤 Data Upload & Management")
inject_custom_css()
st.markdown("Upload CSV files to automatically load customer, ticket, and interaction data into the database.")

st.markdown("<br>", unsafe_allow_html=True)

# ========================================
# SQL QUERY DEMONSTRATION (Module 2.38-2.40)
# ========================================
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 🔍 SQL Query Demonstration")
st.markdown("**Module 2.38-2.40:** Using `db_queries.py` functions to query the database directly with SQL")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📊 Dashboard KPIs (SQL)**")
    if st.button("Run SQL Query: get_dashboard_kpis()", key="sql_kpis"):
        with st.spinner("Executing SQL query..."):
            kpis = get_dashboard_kpis_sql()
            st.success("✅ SQL Query Executed!")
            st.json(kpis)

with col2:
    st.markdown("**🚨 High Risk Customers (SQL)**")
    threshold = st.slider("Risk Score Threshold:", 0, 100, 70, key="risk_threshold")
    if st.button(f"Run SQL Query: get_high_risk_customers({threshold})", key="sql_high_risk"):
        with st.spinner("Executing SQL query..."):
            high_risk = get_high_risk_customers_sql(threshold)
            st.success(f"✅ Found {len(high_risk)} high-risk customers")
            if not high_risk.empty:
                st.dataframe(high_risk[['company_name', 'risk_score', 'arr', 'health_status']].head(5))
            else:
                st.info("No customers above this threshold")

with col3:
    st.markdown("**🎫 Open Tickets (SQL)**")
    priority_filter = st.selectbox("Priority:", [None, "Critical", "High", "Medium", "Low"], key="priority_filter")
    if st.button(f"Run SQL Query: get_open_tickets('{priority_filter}')", key="sql_tickets"):
        with st.spinner("Executing SQL query..."):
            tickets = get_open_tickets_by_priority_sql(priority_filter)
            st.success(f"✅ Found {len(tickets)} open tickets")
            if not tickets.empty:
                st.dataframe(tickets[['ticket_id', 'priority', 'status', 'company_name']].head(5))
            else:
                st.info("No open tickets found")

st.markdown("</div>", unsafe_allow_html=True)

# Show SQL Query Code
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 💻 SQL Query Examples from `db_queries.py`")

tab1, tab2, tab3 = st.tabs(["Dashboard KPIs", "High Risk Customers", "Open Tickets"])

with tab1:
    st.code('''
# SQL Query for Dashboard KPIs
query = """
SELECT 
    ROUND(AVG(risk_score), 1) as avg_risk_score,
    SUM(CASE WHEN health_status = 'Critical' THEN 1 ELSE 0 END) as critical_customers,
    SUM(CASE WHEN health_status = 'Medium' THEN 1 ELSE 0 END) as medium_customers,
    SUM(CASE WHEN health_status = 'Low Risk' THEN 1 ELSE 0 END) as low_risk_customers,
    SUM(CASE WHEN health_status IN ('Critical', 'Medium') THEN arr ELSE 0 END) as revenue_at_risk,
    SUM(arr) as total_arr,
    COUNT(*) as total_customers
FROM customers
"""
''', language='sql')

with tab2:
    st.code('''
# SQL Query for High Risk Customers
query = """
SELECT * FROM vw_high_risk_customers
WHERE risk_score >= ?
ORDER BY arr DESC
"""
params = (min_risk_score,)
''', language='sql')

with tab3:
    st.code('''
# SQL Query for Open Tickets
query = """
SELECT t.*, c.company_name, c.risk_score as customer_risk
FROM tickets t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.status NOT IN ('Resolved', 'Closed')
AND t.priority = ?
ORDER BY t.created_at DESC
"""
''', language='sql')

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Instructions
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 📋 How to Upload Data")
st.markdown("""
**Step 1:** Prepare your CSV files with the correct format  
**Step 2:** Upload files using the file uploaders below  
**Step 3:** Preview the data to verify it looks correct  
**Step 4:** Click "Load to Database" to import the data  

---

**Required CSV Formats:**
- **customers.csv**: customer_id, company_name, industry, arr, contract_type, renewal_date, csm_name
- **tickets.json**: ticket_id, customer_id, subject, priority, status, sentiment, created_date, resolved_date
- **interactions.csv**: interaction_id, customer_id, interaction_type, description, timestamp
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# File uploaders
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Upload Customers CSV")
    customers_file = st.file_uploader("Choose customers CSV file", type=['csv'], key="customers_upload")
    
    if customers_file is not None:
        import io
        customers_uploaded = pd.read_csv(customers_file)
        st.success(f"✅ Loaded {len(customers_uploaded)} customers")
        st.dataframe(customers_uploaded.head(), use_container_width=True)
        
        if st.button("💾 Load Customers to Database", key="load_customers"):
            from db_queries import ChurnGuardDB
            import sqlite3
            
            conn = sqlite3.connect('churnguard.db')
            cursor = conn.cursor()
            
            try:
                # Clear existing customers
                cursor.execute("DELETE FROM customers")
                
                # Insert new customers
                for _, row in customers_uploaded.iterrows():
                    cursor.execute("""
                        INSERT INTO customers (
                            company_name, industry, arr, 
                            renewal_date, health_status, risk_score, sentiment
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row['company_name'],
                        row['industry'],
                        int(row['arr']),
                        row['renewal_date'],
                        'Low Risk',
                        20,
                        'Neutral'
                    ))
                
                conn.commit()
                conn.close()
                
                st.success(f"🎉 Successfully loaded {len(customers_uploaded)} customers into database!")
                st.info("🔄 Refresh the page to see updated data in dashboards")
                
                # Clear cache to reload data
                st.cache_data.clear()
                
            except Exception as e:
                st.error(f"❌ Error loading customers: {str(e)}")
                conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 🎫 Upload Tickets JSON")
    tickets_file = st.file_uploader("Choose tickets JSON file", type=['json'], key="tickets_upload")
    
    if tickets_file is not None:
        import json
        import io
        tickets_uploaded = json.load(tickets_file)
        tickets_df_uploaded = pd.DataFrame(tickets_uploaded)
        st.success(f"✅ Loaded {len(tickets_df_uploaded)} tickets")
        st.dataframe(tickets_df_uploaded.head(), use_container_width=True)
        
        if st.button("💾 Load Tickets to Database", key="load_tickets"):
            from db_queries import ChurnGuardDB
            import sqlite3
            
            conn = sqlite3.connect('churnguard.db')
            cursor = conn.cursor()
            
            try:
                # Clear existing tickets
                cursor.execute("DELETE FROM tickets")
                
                # Insert tickets
                for ticket in tickets_uploaded:
                    # Map customer_id
                    cust_id_str = ticket['customer_id']
                    if isinstance(cust_id_str, str) and 'CUST-' in cust_id_str:
                        cust_id = int(cust_id_str.replace('CUST-', ''))
                    else:
                        cust_id = 1
                    
                    cursor.execute("""
                        INSERT INTO tickets (
                            ticket_id, customer_id, subject, description,
                            priority, status, sentiment, category,
                            created_at, resolved_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        ticket['ticket_id'],
                        cust_id,
                        ticket['subject'],
                        ticket.get('subject', 'No description'),
                        ticket['priority'],
                        ticket['status'],
                        ticket['sentiment'],
                        'Support',
                        ticket['created_date'],
                        ticket.get('resolved_date')
                    ))
                
                conn.commit()
                conn.close()
                
                st.success(f"🎉 Successfully loaded {len(tickets_uploaded)} tickets into database!")
                st.info("🔄 Refresh the page to see updated data in dashboards")
                
                # Clear cache
                st.cache_data.clear()
                
            except Exception as e:
                st.error(f"❌ Error loading tickets: {str(e)}")
                conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Interactions upload (full width)
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 💬 Upload Interactions CSV")
interactions_file = st.file_uploader("Choose interactions CSV file", type=['csv'], key="interactions_upload")

if interactions_file is not None:
    interactions_uploaded = pd.read_csv(interactions_file)
    st.success(f"✅ Loaded {len(interactions_uploaded)} interactions")
    
    col_preview, col_button = st.columns([3, 1])
    with col_preview:
        st.dataframe(interactions_uploaded.head(10), use_container_width=True)
    
    with col_button:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("💾 Load Interactions to Database", key="load_interactions"):
            from db_queries import ChurnGuardDB
            import sqlite3
            
            conn = sqlite3.connect('churnguard.db')
            cursor = conn.cursor()
            
            try:
                # Clear existing interactions
                cursor.execute("DELETE FROM interactions")
                
                # Insert interactions
                for _, row in interactions_uploaded.iterrows():
                    # Map customer_id
                    cust_id_str = row['customer_id']
                    if isinstance(cust_id_str, str) and 'CUST-' in cust_id_str:
                        cust_id = int(cust_id_str.replace('CUST-', ''))
                    else:
                        cust_id = 1
                    
                    # Map interaction types
                    interaction_type = row['interaction_type']
                    type_mapping = {
                        'Login': 'Email',
                        'Feature Usage': 'Training',
                        'Support Call': 'Call',
                        'QBR': 'QBR',
                        'Email Sent': 'Email'
                    }
                    mapped_type = type_mapping.get(interaction_type, 'Email')
                    
                    cursor.execute("""
                        INSERT INTO interactions (
                            customer_id, interaction_type,
                            interaction_date, notes
                        ) VALUES (?, ?, ?, ?)
                    """, (
                        cust_id,
                        mapped_type,
                        row['timestamp'],
                        row['description']
                    ))
                
                conn.commit()
                conn.close()
                
                st.success(f"🎉 Successfully loaded {len(interactions_uploaded)} interactions into database!")
                st.info("🔄 Refresh the page to see updated data in dashboards")
                
                # Clear cache
                st.cache_data.clear()
                
            except Exception as e:
                st.error(f"❌ Error loading interactions: {str(e)}")
                conn.close()

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Current database status
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 📊 Current Database Status")

from db_queries import ChurnGuardDB
db = ChurnGuardDB('churnguard.db')

col1, col2, col3 = st.columns(3)

with col1:
    customer_count = db.execute_query("SELECT COUNT(*) as count FROM customers")['count'][0]
    st.metric("Customers in Database", customer_count)

with col2:
    ticket_count = db.execute_query("SELECT COUNT(*) as count FROM tickets")['count'][0]
    st.metric("Tickets in Database", ticket_count)

with col3:
    interaction_count = db.execute_query("SELECT COUNT(*) as count FROM interactions")['count'][0]
    st.metric("Interactions in Database", interaction_count)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Download sample templates
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 📥 Download Sample Templates")
st.markdown("Need help with the CSV format? Download these sample templates:")

col1, col2, col3 = st.columns(3)

with col1:
    sample_customers = pd.DataFrame({
        'customer_id': ['CUST-1001', 'CUST-1002'],
        'company_name': ['Acme Corp', 'TechStart Inc'],
        'industry': ['Tech', 'Finance'],
        'arr': [250000, 150000],
        'contract_type': ['Annual', 'Monthly'],
        'renewal_date': ['2026-12-31', '2026-11-30'],
        'csm_name': ['Alice', 'Bob']
    })
    csv_customers = sample_customers.to_csv(index=False)
    st.download_button(
        label="📄 Download customers.csv",
        data=csv_customers,
        file_name="sample_customers.csv",
        mime="text/csv"
    )

with col2:
    st.markdown("**tickets.json template**")
    st.code('''[
{
"ticket_id": "TKT-001",
"customer_id": "CUST-1001",
"subject": "API timeout",
"priority": "High",
"status": "Open",
"sentiment": "Negative",
"created_date": "2026-08-01T10:00:00",
"resolved_date": null
}
]''', language='json')

with col3:
    sample_interactions = pd.DataFrame({
        'interaction_id': ['INT-5001', 'INT-5002'],
        'customer_id': ['CUST-1001', 'CUST-1002'],
        'interaction_type': ['QBR', 'Support Call'],
        'description': ['Quarterly review', 'Technical support'],
        'timestamp': ['2026-08-01 14:00:00', '2026-08-02 10:30:00']
    })
    csv_interactions = sample_interactions.to_csv(index=False)
    st.download_button(
        label="📄 Download interactions.csv",
        data=csv_interactions,
        file_name="sample_interactions.csv",
        mime="text/csv"
    )

st.markdown('</div>', unsafe_allow_html=True)
