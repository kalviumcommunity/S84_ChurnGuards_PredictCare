# pyrefly: ignore [missing-import]
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

# Custom CSS matching Stitch design tokens
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap');
    @import url("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap");
    
    html, body, p, div, span, a, h1, h2, h3, h4, h5, h6, li, label, .stMarkdown {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1b1b1d; /* on-background */
    }
    
    .main { background-color: #fcf8fa; padding: 2rem; }
    .stApp { background-color: #fcf8fa; }
    
    /* Hide the native footer */
    footer { display: none; }
    
    /* Sidebar styling to match Stitch */
    [data-testid="stSidebar"] {
        background-color: #f0edef; /* surface-container */
        border-right: 1px solid #c6c6cd; /* outline-variant */
        padding-top: 1rem;
        box-shadow: none;
    }
    
    /* Target text inside sidebar */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div {
        color: #45464d !important; /* on-surface-variant */
    }
    
    [data-testid="stSidebarNav"] a { border-radius: 4px; margin: 4px 12px; }
    [data-testid="stSidebarNav"] a:hover { background-color: #e4e2e4 !important; }
    [data-testid="stSidebarNav"] a[aria-current="page"] { 
        background-color: transparent !important; 
        border-right: 4px solid #000000;
        border-radius: 0;
        color: #000000 !important;
        font-weight: 700;
    }
    [data-testid="stSidebarNav"] span { color: #000000 !important; font-weight: 500; font-size: 14px; }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #F8FAFC !important; /* White for radio labels */
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
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
    
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 32px;
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0px 10px 15px -3px rgba(15, 23, 42, 0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Authentication State
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 10vh;">
            <div style="max-width: 400px; width: 100%; padding: 40px; background: white; border-radius: 16px; border: 1px solid #c6c6cd; box-shadow: 0px 10px 25px -5px rgba(0,0,0,0.05); text-align: center;">
                <div style="width: 48px; height: 48px; background-color: #1a73e8; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 20px; margin-bottom: 16px;">📊</div>
                <h1 style="font-size: 24px !important; margin-bottom: 8px !important;">Welcome to ChurnGuard AI</h1>
                <p style="color: #737373 !important; font-size: 14px; margin-bottom: 32px;">Please sign in or create an account to continue.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Center the forms
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔒 Sign In", "✨ Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username", value="admin")
                password = st.text_input("Password", type="password", value="admin")
                submitted = st.form_submit_button("Sign In", use_container_width=True)
                
                if submitted:
                    if username == "admin" and password == "admin":
                        with st.spinner("Authenticating..."):
                            import time
                            time.sleep(1)
                        st.toast("Welcome back, Admin!", icon="👋")
                        time.sleep(0.5)
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please use admin/admin.")
                        
        with tab2:
            with st.form("signup_form"):
                st.text_input("Email Address", placeholder="name@company.com")
                st.text_input("Username", placeholder="Choose a username")
                st.text_input("Password", type="password", placeholder="Create a password")
                signup_submitted = st.form_submit_button("Create Account", use_container_width=True)
                
                if signup_submitted:
                    with st.spinner("Provisioning enterprise workspace..."):
                        import time
                        time.sleep(1.5)
                    st.success("Workspace provisioned successfully!")
                    st.toast("Routing to dashboard...", icon="🔄")
                    time.sleep(1)
                    st.session_state.authenticated = True
                    st.rerun()

# Pages definition
dashboard = st.Page("app_pages/1_dashboard.py", title="Executive Dashboard", icon="📊", default=True)
risk_center = st.Page("app_pages/2_risk_center.py", title="Risk Command Center", icon="🚨")
ticket_workspace = st.Page("app_pages/3_ticket_workspace.py", title="Ticket Workspace", icon="🎫")
directory = st.Page("app_pages/4_directory.py", title="Customer Directory", icon="👥")
data_upload = st.Page("app_pages/5_data_upload.py", title="Data Upload", icon="📥")

if not st.session_state.authenticated:
    # Hide sidebar when not authenticated
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none; }
        </style>
    """, unsafe_allow_html=True)
    
    # Render login page
    login_page = st.Page(login, title="Log In", icon="🔒")
    pg = st.navigation([login_page])
    pg.run()
    
else:
    # Custom Sidebar Branding
    with st.sidebar:
        st.markdown("""
        <div style="padding: 0 1rem 2rem 1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 32px; height: 32px; background-color: #1a73e8; border-radius: 6px; 
                            display: flex; align-items: center; justify-content: center; color: white; 
                            font-weight: 700; font-size: 14px;">📊</div>
                <div>
                    <div style="font-size: 16px; font-weight: 700; color: #0F172A;">ChurnGuard AI</div>
                    <div style="font-size: 11px; color: #64748B;">Enterprise Analytics</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add a logout button at the bottom of the sidebar
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Log Out", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
            
    # Run navigation with actual pages
    pg = st.navigation({
        "Modules": [dashboard, risk_center, ticket_workspace, directory],
        "Settings": [data_upload]
    })
    pg.run()
