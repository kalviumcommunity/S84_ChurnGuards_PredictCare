import streamlit as st

# Page configuration
st.set_page_config(
    page_title="ChurnGuard AI - Enterprise Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "ChurnGuard AI - Customer Churn Prevention System"
    }
)

# Custom CSS matching the exact design screenshots
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .main {
        background-color: #f8fafc; /* Slate 50 */
        padding: 2rem;
    }
    
    .stApp {
        background-color: #f8fafc;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0F172A; /* Deep Navy from Stitch Design */
        border-right: 1px solid #1E293B; /* Dark Slate */
        padding-top: 1rem;
    }
    
    /* Target text inside sidebar to be light colored */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] .st-emotion-cache-16idsys p {
        color: #94A3B8 !important; /* Muted grey */
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #F8FAFC !important; /* White for radio labels */
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    h1 {
        color: #0F172A !important; /* Deep Navy */
        font-size: 32px !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #0F172A !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        color: #0F172A !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    p, span, label, div {
        color: #475569 !important; /* Slate 600 */
    }
    
    .content-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0px 4px 6px -1px rgba(15, 23, 42, 0.1);
    }
    
    .btn-primary {
        background-color: #0F172A;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        border: none;
        font-weight: 500;
        font-size: 14px;
        text-decoration: none;
        display: inline-block;
        transition: background-color 0.2s;
    }
    
    .btn-primary:hover {
        background-color: #1e293b; /* Slate 800 */
    }
</style>
""", unsafe_allow_html=True)

# Custom Sidebar Branding
with st.sidebar:
    st.markdown("""
    <div style="padding: 0 1rem 2rem 1rem; border-bottom: 1px solid #1E293B; margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 32px; height: 32px; background-color: #3B82F6; border-radius: 6px; 
                        display: flex; align-items: center; justify-content: center; color: white; 
                        font-weight: 700; font-size: 14px;">📊</div>
            <div>
                <div style="font-size: 16px; font-weight: 700; color: #FFFFFF;">ChurnGuard AI</div>
                <div style="font-size: 11px; color: #94A3B8;">Enterprise Analytics</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main Welcome Page
st.title("Welcome to ChurnGuard AI")
st.markdown("### The Enterprise Customer Churn Prevention System")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="content-card">
    <h3>🚀 Get Started</h3>
    <p>Please use the sidebar on the left to navigate to the various modules of the application:</p>
    <ul>
        <li><b>Executive Dashboard:</b> Real-time overview of churn risk and retention performance.</li>
        <li><b>Risk Command Center:</b> Monitor and manage customer risk alerts.</li>
        <li><b>Ticket Workspace:</b> Handle high-priority customer support tickets.</li>
        <li><b>Customer Directory:</b> Search and view detailed customer profiles.</li>
        <li><b>Data Upload:</b> Import new CSV/JSON data into the database.</li>
    </ul>
    <br>
    <a href="#" class="btn-primary" onclick="window.parent.document.querySelector('a[href*=\'1_dashboard\']').click(); return false;">Go to Dashboard →</a>
</div>
""", unsafe_allow_html=True)
