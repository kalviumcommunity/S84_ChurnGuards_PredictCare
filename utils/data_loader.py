import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def calculate_real_risk_score(customer_row, tickets_df, interactions_df):
    """
    Calculate real risk score based on multiple business factors
    
    Risk Components:
    1. Open Tickets (0-25 points)
    2. Last Login Activity (0-20 points)
    3. Sentiment Analysis (0-25 points)
    4. Days Until Renewal (0-20 points)
    5. CSAT Score (0-10 points)
    
    Returns: Risk score from 0-100 (higher = more at risk)
    """
    risk_score = 0
    customer_id = customer_row['customer_id']
    
    # 1. OPEN TICKETS RISK (0-25 points)
    if not tickets_df.empty:
        customer_tickets = tickets_df[tickets_df['customer_id'] == customer_id]
        open_tickets = customer_tickets[customer_tickets['status'].isin(['Open', 'In Progress'])]
        critical_tickets = open_tickets[open_tickets['priority'] == 'Critical']
        
        # Count critical tickets (15 points per critical ticket, max 15)
        risk_score += min(len(critical_tickets) * 5, 15)
        
        # Count all open tickets (2 points per ticket, max 10)
        risk_score += min(len(open_tickets) * 2, 10)
    
    # 2. LAST LOGIN ACTIVITY RISK (0-20 points)
    if pd.notna(customer_row.get('last_activity')):
        try:
            last_activity = pd.to_datetime(customer_row['last_activity'])
            days_since_login = (datetime.now() - last_activity).days
            
            if days_since_login > 30:
                risk_score += 20  # No activity in 30+ days = max risk
            elif days_since_login > 14:
                risk_score += 15  # No activity in 2+ weeks
            elif days_since_login > 7:
                risk_score += 10  # No activity in 1+ week
            elif days_since_login > 3:
                risk_score += 5   # Limited activity
        except:
            risk_score += 10  # Invalid date = moderate risk
    else:
        risk_score += 10  # No activity data = moderate risk
    
    # 3. SENTIMENT ANALYSIS RISK (0-25 points)
    sentiment = customer_row.get('sentiment', 'Neutral')
    if sentiment == 'Negative':
        risk_score += 25
    elif sentiment == 'Neutral':
        risk_score += 10
    # Positive = 0 points
    
    # Check recent interaction sentiment if available
    if not interactions_df.empty:
        recent_interactions = interactions_df[
            (interactions_df['customer_id'] == customer_id) &
            (interactions_df['interaction_type'].isin(['Support Email', 'Phone Call']))
        ].tail(5)
        
        if not recent_interactions.empty:
            negative_count = len(recent_interactions[recent_interactions.get('sentiment') == 'Negative'])
            if negative_count >= 3:
                risk_score += 5  # Multiple negative interactions
    
    # 4. DAYS UNTIL RENEWAL RISK (0-20 points)
    if pd.notna(customer_row.get('renewal_date')):
        try:
            renewal_date = pd.to_datetime(customer_row['renewal_date'])
            days_until_renewal = (renewal_date - datetime.now()).days
            
            if days_until_renewal < 0:
                risk_score += 20  # Past renewal date = critical
            elif days_until_renewal <= 30:
                risk_score += 15  # Renewal within 30 days
            elif days_until_renewal <= 60:
                risk_score += 10  # Renewal within 60 days
            elif days_until_renewal <= 90:
                risk_score += 5   # Renewal within 90 days
        except:
            risk_score += 5  # Invalid date = slight risk
    else:
        risk_score += 5  # No renewal data = slight risk
    
    # 5. CSAT SCORE RISK (0-10 points)
    csat_score = customer_row.get('csat_score', 5)
    try:
        csat = float(csat_score)
        if csat <= 2.0:
            risk_score += 10  # Very low satisfaction
        elif csat <= 3.0:
            risk_score += 7   # Low satisfaction
        elif csat <= 4.0:
            risk_score += 3   # Below average
        # Above 4.0 = 0 points
    except:
        risk_score += 5  # Invalid CSAT = moderate risk
    
    # Cap risk score at 100
    risk_score = min(risk_score, 100)
    
    return int(risk_score)


def calculate_health_status(risk_score):
    """Convert risk score to health status category"""
    if risk_score >= 70:
        return 'Critical'
    elif risk_score >= 50:
        return 'Medium'
    else:
        return 'Low Risk'


@st.cache_data
def load_data():
    """
    Load data from SQLite database instead of CSV files
    This connects the database to the frontend!
    """
    from db_queries import ChurnGuardDB
    
    db = ChurnGuardDB('churnguard.db')
    
    # Load customers from database
    customers = db.execute_query("SELECT * FROM customers")
    
    # Load tickets from database (no JOIN for now, IDs don't match)
    tickets = db.execute_query("SELECT * FROM tickets")
    
    # Load interactions from database  
    interactions = db.execute_query("SELECT * FROM interactions")
    
    # Rename columns to match expected format
    if not interactions.empty and 'interaction_date' in interactions.columns:
        interactions['timestamp'] = interactions['interaction_date']
    
    # Create empty churn_history (not in database yet)
    churn_history = pd.DataFrame()
    
    # Add computed columns for compatibility with existing UI
    if not customers.empty:
        customers['arr'] = customers['arr'].astype(float)
        customers['last_activity'] = pd.to_datetime(customers['last_activity'], errors='coerce')
        customers['company_name'] = customers['company_name'].astype(str)
        
    if not tickets.empty:
        tickets['customer'] = 'User ' + tickets['customer_id'].astype(str)
        tickets['company'] = 'Company ' + tickets['customer_id'].astype(str)
        tickets['risk_score'] = tickets.get('risk_score', 50)
    
    # Apply real risk calculation to all customers
    if not customers.empty:
        customers['risk_score'] = customers.apply(
            lambda row: calculate_real_risk_score(row, tickets, interactions), 
            axis=1
        )
        customers['health_status'] = customers['risk_score'].apply(calculate_health_status)

    return customers, tickets, interactions, churn_history


def filter_customers_by_risk(df, risk_filter):
    """Filter customers based on selected risk levels"""
    if "All Levels" in risk_filter:
        return df
    return df[df['health_status'].isin(risk_filter)]


def calculate_churn_probability(risk_score):
    """Convert risk score to churn probability percentage"""
    if risk_score >= 80:
        return "Very High (>70%)"
    elif risk_score >= 60:
        return "High (50-70%)"
    elif risk_score >= 40:
        return "Medium (30-50%)"
    else:
        return "Low (<30%)"


def get_risk_alert_summary(customers_df):
    """Generate real-time risk alert summary with priority classification"""
    alerts = []
    
    for idx, customer in customers_df.iterrows():
        # High risk score alert
        if customer['risk_score'] >= 80:
            alerts.append({
                'severity': 'Critical',
                'company': customer['company_name'],
                'alert': f"Risk score jumped to {customer['risk_score']}",
                'detail': 'Immediate intervention required',
                'arr': customer['arr'],
                'icon': 'π¨'
            })
        
        # Negative sentiment alert
        if customer['sentiment'] == 'Negative' and customer['health_status'] == 'Critical':
            alerts.append({
                'severity': 'High',
                'company': customer['company_name'],
                'alert': 'Negative sentiment with critical health status',
                'detail': 'Customer satisfaction at risk',
                'arr': customer['arr'],
                'icon': 'π'
            })
        
        # Low activity alert
        if pd.notna(customer['last_activity']):
            days_since_activity = (datetime.now() - customer['last_activity']).days
            if days_since_activity > 14 and customer['risk_score'] > 60:
                alerts.append({
                    'severity': 'Medium',
                    'company': customer['company_name'],
                    'alert': f"No activity for {days_since_activity} days",
                    'detail': 'Engagement drop detected',
                    'arr': customer['arr'],
                    'icon': 'π“‰'
                })
    
    # Sort by severity and ARR
    severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
    alerts_sorted = sorted(alerts, key=lambda x: (severity_order.get(x['severity'], 4), -x['arr']))
    
    return alerts_sorted[:10]


def export_customer_data(customers_df):
    """Export customer data with risk metrics and health status"""
    export_data = customers_df[['customer_id', 'company_name', 'risk_score', 'arr', 'health_status', 'sentiment']].copy()
    export_data['last_activity'] = customers_df['last_activity'].dt.strftime('%Y-%m-%d')
    csv = export_data.to_csv(index=False)
    return csv


# SQL QUERY FUNCTIONS (Module 2.38-2.40)
@st.cache_data
def get_high_risk_customers_sql(threshold=70):
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_high_risk_customers(min_risk_score=threshold)

@st.cache_data  
def get_open_tickets_by_priority_sql(priority=None):
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_open_tickets(priority=priority)

@st.cache_data
def get_dashboard_kpis_sql():
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_dashboard_kpis()

@st.cache_data
def get_revenue_at_risk_sql():
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_revenue_at_risk()

@st.cache_data
def get_ticket_metrics_sql():
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_ticket_metrics()

@st.cache_data
def search_customers_sql(search_term):
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.search_customers(search_term)

@st.cache_data
def get_renewal_pipeline_sql(days_ahead=90):
    from db_queries import ChurnGuardDB
    db = ChurnGuardDB('churnguard.db')
    return db.get_renewal_pipeline(days_ahead=days_ahead)

 d e f   i n j e c t _ c u s t o m _ c s s ( ) : 
         s t . m a r k d o w n ( " " " 
         < s t y l e > 
                 @ i m p o r t   u r l ( " h t t p s : / / f o n t s . g o o g l e a p i s . c o m / c s s 2 ? f a m i l y = I n t e r : w g h t @ 3 0 0 ; 4 0 0 ; 5 0 0 ; 6 0 0 ; 7 0 0 & d i s p l a y = s w a p " ) ; 
                 *   {   f o n t - f a m i l y :   " I n t e r " ,   - a p p l e - s y s t e m ,   B l i n k M a c S y s t e m F o n t ,   s a n s - s e r i f   ! i m p o r t a n t ;   } 
                 . m a i n   {   b a c k g r o u n d - c o l o r :   # f 8 f a f c ;   p a d d i n g :   2 r e m ;   } 
                 . s t A p p   {   b a c k g r o u n d - c o l o r :   # f 8 f a f c ;   } 
                 [ d a t a - t e s t i d = " s t S i d e b a r " ]   {   b a c k g r o u n d - c o l o r :   # 0 F 1 7 2 A ;   b o r d e r - r i g h t :   1 p x   s o l i d   # 1 E 2 9 3 B ;   p a d d i n g - t o p :   1 r e m ;   } 
                 [ d a t a - t e s t i d = " s t S i d e b a r " ]   p ,   [ d a t a - t e s t i d = " s t S i d e b a r " ]   s p a n ,   [ d a t a - t e s t i d = " s t S i d e b a r " ]   l a b e l ,   [ d a t a - t e s t i d = " s t S i d e b a r " ]   d i v ,   [ d a t a - t e s t i d = " s t S i d e b a r " ]   . s t - e m o t i o n - c a c h e - 1 6 i d s y s   p   {   c o l o r :   # 9 4 A 3 B 8   ! i m p o r t a n t ;   } 
                 . b l o c k - c o n t a i n e r   {   p a d d i n g - t o p :   1 r e m ;   p a d d i n g - b o t t o m :   1 r e m ;   m a x - w i d t h :   1 0 0 % ;   } 
                 h 1   {   c o l o r :   # 0 F 1 7 2 A   ! i m p o r t a n t ;   f o n t - s i z e :   3 2 p x   ! i m p o r t a n t ;   f o n t - w e i g h t :   7 0 0   ! i m p o r t a n t ;   m a r g i n - b o t t o m :   0 . 5 r e m   ! i m p o r t a n t ;   } 
                 h 2   {   c o l o r :   # 0 F 1 7 2 A   ! i m p o r t a n t ;   f o n t - s i z e :   1 8 p x   ! i m p o r t a n t ;   f o n t - w e i g h t :   6 0 0   ! i m p o r t a n t ;   m a r g i n - b o t t o m :   1 r e m   ! i m p o r t a n t ;   } 
                 h 3   {   c o l o r :   # 0 F 1 7 2 A   ! i m p o r t a n t ;   f o n t - s i z e :   1 6 p x   ! i m p o r t a n t ;   f o n t - w e i g h t :   6 0 0   ! i m p o r t a n t ;   } 
                 p ,   s p a n ,   l a b e l ,   d i v   {   c o l o r :   # 4 7 5 5 6 9   ! i m p o r t a n t ;   } 
                 . m e t r i c - c a r d   {   b a c k g r o u n d - c o l o r :   # f f f f f f ;   b o r d e r :   1 p x   s o l i d   # e 2 e 8 f 0 ;   b o r d e r - r a d i u s :   6 p x ;   p a d d i n g :   2 0 p x ;   m a r g i n - b o t t o m :   1 6 p x ;   b o x - s h a d o w :   0 p x   4 p x   6 p x   - 1 p x   r g b a ( 1 5 ,   2 3 ,   4 2 ,   0 . 1 ) ;   t r a n s i t i o n :   t r a n s f o r m   0 . 2 s ,   b o x - s h a d o w   0 . 2 s ;   } 
                 . m e t r i c - c a r d : h o v e r   {   t r a n s f o r m :   t r a n s l a t e Y ( - 2 p x ) ;   b o x - s h a d o w :   0 p x   1 0 p x   1 5 p x   - 3 p x   r g b a ( 1 5 ,   2 3 ,   4 2 ,   0 . 1 ) ;   } 
                 . m e t r i c - l a b e l   {   f o n t - s i z e :   1 2 p x ;   c o l o r :   # 6 4 7 4 8 B ;   f o n t - w e i g h t :   6 0 0 ;   t e x t - t r a n s f o r m :   u p p e r c a s e ;   l e t t e r - s p a c i n g :   0 . 5 p x ;   m a r g i n - b o t t o m :   8 p x ;   } 
                 . m e t r i c - v a l u e   {   f o n t - s i z e :   3 6 p x ;   f o n t - w e i g h t :   7 0 0 ;   c o l o r :   # 0 F 1 7 2 A ;   l i n e - h e i g h t :   1 ;   f o n t - v a r i a n t - n u m e r i c :   t a b u l a r - n u m s ;   } 
                 . m e t r i c - c h a n g e   {   f o n t - s i z e :   1 3 p x ;   f o n t - w e i g h t :   6 0 0 ;   m a r g i n - t o p :   8 p x ;   } 
                 . p o s i t i v e   {   c o l o r :   # 1 0 B 9 8 1 ;   }   . n e g a t i v e   {   c o l o r :   # D C 2 6 2 6 ;   } 
                 . b a d g e   {   d i s p l a y :   i n l i n e - b l o c k ;   p a d d i n g :   4 p x   1 2 p x ;   b o r d e r - r a d i u s :   4 p x ;   f o n t - s i z e :   1 2 p x ;   f o n t - w e i g h t :   5 0 0 ;   } 
                 . b a d g e - c r i t i c a l   {   b a c k g r o u n d - c o l o r :   # f e f 2 f 2 ;   c o l o r :   # D C 2 6 2 6 ;   b o r d e r :   1 p x   s o l i d   # f e c a c a ;   } 
                 . b a d g e - h i g h   {   b a c k g r o u n d - c o l o r :   # f f f b e b ;   c o l o r :   # F 5 9 E 0 B ;   b o r d e r :   1 p x   s o l i d   # f d e 6 8 a ;   } 
                 . b a d g e - m e d i u m   {   b a c k g r o u n d - c o l o r :   # f 8 f a f c ;   c o l o r :   # 6 4 7 4 8 B ;   b o r d e r :   1 p x   s o l i d   # e 2 e 8 f 0 ;   } 
                 . b a d g e - l o w   {   b a c k g r o u n d - c o l o r :   # e c f d f 5 ;   c o l o r :   # 1 0 B 9 8 1 ;   b o r d e r :   1 p x   s o l i d   # a 7 f 3 d 0 ;   } 
                 . c o n t e n t - c a r d   {   b a c k g r o u n d - c o l o r :   # f f f f f f ;   b o r d e r :   1 p x   s o l i d   # e 2 e 8 f 0 ;   b o r d e r - r a d i u s :   8 p x ;   p a d d i n g :   2 4 p x ;   m a r g i n - b o t t o m :   1 6 p x ;   b o x - s h a d o w :   0 p x   4 p x   6 p x   - 1 p x   r g b a ( 1 5 ,   2 3 ,   4 2 ,   0 . 1 ) ;   } 
                 . b t n - p r i m a r y   {   b a c k g r o u n d - c o l o r :   # 0 F 1 7 2 A ;   c o l o r :   w h i t e ;   p a d d i n g :   8 p x   1 6 p x ;   b o r d e r - r a d i u s :   6 p x ;   b o r d e r :   n o n e ;   f o n t - w e i g h t :   5 0 0 ;   f o n t - s i z e :   1 4 p x ;   t e x t - d e c o r a t i o n :   n o n e ;   d i s p l a y :   i n l i n e - b l o c k ;   t r a n s i t i o n :   b a c k g r o u n d - c o l o r   0 . 2 s ;   } 
                 . b t n - p r i m a r y : h o v e r   {   b a c k g r o u n d - c o l o r :   # 1 e 2 9 3 b ;   } 
                 . b t n - s e c o n d a r y   {   b a c k g r o u n d - c o l o r :   w h i t e ;   c o l o r :   # 0 F 1 7 2 A ;   p a d d i n g :   8 p x   1 6 p x ;   b o r d e r - r a d i u s :   6 p x ;   b o r d e r :   1 p x   s o l i d   # e 2 e 8 f 0 ;   f o n t - w e i g h t :   5 0 0 ;   f o n t - s i z e :   1 4 p x ;   t e x t - d e c o r a t i o n :   n o n e ;   d i s p l a y :   i n l i n e - b l o c k ;   t r a n s i t i o n :   b a c k g r o u n d - c o l o r   0 . 2 s ;   } 
                 . b t n - s e c o n d a r y : h o v e r   {   b a c k g r o u n d - c o l o r :   # f 1 f 5 f 9 ;   } 
                 . d a t a - t a b l e   {   w i d t h :   1 0 0 % ;   b o r d e r - c o l l a p s e :   c o l l a p s e ;   } 
                 . d a t a - t a b l e   t h   {   t e x t - a l i g n :   l e f t ;   p a d d i n g :   1 2 p x ;   f o n t - s i z e :   1 2 p x ;   f o n t - w e i g h t :   6 0 0 ;   c o l o r :   # 6 4 7 4 8 B ;   t e x t - t r a n s f o r m :   u p p e r c a s e ;   l e t t e r - s p a c i n g :   0 . 5 p x ;   b o r d e r - b o t t o m :   1 p x   s o l i d   # e 2 e 8 f 0 ;   } 
                 . d a t a - t a b l e   t d   {   p a d d i n g :   1 6 p x   1 2 p x ;   b o r d e r - b o t t o m :   1 p x   s o l i d   # f 8 f a f c ;   f o n t - s i z e :   1 4 p x ;   c o l o r :   # 0 F 1 7 2 A ;   f o n t - v a r i a n t - n u m e r i c :   t a b u l a r - n u m s ;   } 
         < / s t y l e > 
         " " " ,   u n s a f e _ a l l o w _ h t m l = T r u e ) 
         
         w i t h   s t . s i d e b a r : 
                 s t . m a r k d o w n ( " " " 
                 < d i v   s t y l e = " p a d d i n g :   0   1 r e m   2 r e m   1 r e m ;   b o r d e r - b o t t o m :   1 p x   s o l i d   # 1 E 2 9 3 B ;   m a r g i n - b o t t o m :   1 . 5 r e m ; " > 
                         < d i v   s t y l e = " d i s p l a y :   f l e x ;   a l i g n - i t e m s :   c e n t e r ;   g a p :   1 2 p x ; " > 
                                 < d i v   s t y l e = " w i d t h :   3 2 p x ;   h e i g h t :   3 2 p x ;   b a c k g r o u n d - c o l o r :   # 3 B 8 2 F 6 ;   b o r d e r - r a d i u s :   6 p x ;   
                                                         d i s p l a y :   f l e x ;   a l i g n - i t e m s :   c e n t e r ;   j u s t i f y - c o n t e n t :   c e n t e r ;   c o l o r :   w h i t e ;   
                                                         f o n t - w e i g h t :   7 0 0 ;   f o n t - s i z e :   1 4 p x ; " > =ΨΚά< / d i v > 
                                 < d i v > 
                                         < d i v   s t y l e = " f o n t - s i z e :   1 6 p x ;   f o n t - w e i g h t :   7 0 0 ;   c o l o r :   # F F F F F F ; " > C h u r n G u a r d   A I < / d i v > 
                                         < d i v   s t y l e = " f o n t - s i z e :   1 1 p x ;   c o l o r :   # 9 4 A 3 B 8 ; " > E n t e r p r i s e   A n a l y t i c s < / d i v > 
                                 < / d i v > 
                         < / d i v > 
                 < / d i v > 
                 " " " ,   u n s a f e _ a l l o w _ h t m l = T r u e ) 
  
 