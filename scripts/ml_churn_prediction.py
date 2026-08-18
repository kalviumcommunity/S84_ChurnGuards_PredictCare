import os
import sqlite3
import pandas as pd
import numpy as np
import joblib
import logging
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'churnguard.db')
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

def load_training_data():
    """Load data for training from the database."""
    conn = sqlite3.connect(DB_PATH)
    
    # We will simulate a historical dataset from current customers.
    # In a real scenario, this would come from a snapshot or a churn_history table with features.
    # For now, we will use existing customers and simulate a target 'is_churned' for training.
    
    query = '''
    SELECT c.customer_id, c.arr, c.risk_score, c.health_status, 
           c.sentiment, c.industry
    FROM customers c
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Feature engineering for ML
    df['arr_log'] = np.log1p(df['arr'])
    df['sentiment_score'] = df['sentiment'].map({'Positive': 1, 'Neutral': 0, 'Negative': -1}).fillna(0)
    
    # One-hot encode industry
    industry_dummies = pd.get_dummies(df['industry'], prefix='ind', drop_first=True)
    df = pd.concat([df, industry_dummies], axis=1)
    
    # Simulate historical targets for training (for demonstration)
    np.random.seed(42)
    # Higher risk score -> higher chance of being simulated as churned
    df['is_churned'] = (np.random.rand(len(df)) < (df['risk_score'] / 100)).astype(int)
    # CLV is roughly ARR * random multiplier (1 to 5)
    df['historical_clv'] = df['arr'] * np.random.uniform(1.0, 5.0, len(df))
    
    return df

def train_and_save_models(df):
    """Train ML models and save them to disk."""
    features = ['arr_log', 'risk_score', 'sentiment_score'] + [col for col in df.columns if col.startswith('ind_')]
    
    X = df[features]
    y_churn = df['is_churned']
    y_clv = df['historical_clv']
    
    # 1. Churn Prediction Model (Random Forest)
    churn_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42))
    ])
    churn_pipeline.fit(X, y_churn)
    joblib.dump(churn_pipeline, os.path.join(MODELS_DIR, 'churn_model.pkl'))
    logger.info("Trained and saved Churn Prediction Model.")
    
    # 2. CLV Forecasting Model (Ridge Regression)
    clv_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', Ridge(alpha=1.0))
    ])
    clv_pipeline.fit(X, y_clv)
    joblib.dump(clv_pipeline, os.path.join(MODELS_DIR, 'clv_model.pkl'))
    logger.info("Trained and saved CLV Forecasting Model.")
    
    # 3. Anomaly Detection (Isolation Forest)
    anomaly_model = Pipeline([
        ('scaler', StandardScaler()),
        ('detector', IsolationForest(contamination=0.05, random_state=42))
    ])
    anomaly_model.fit(X)
    joblib.dump(anomaly_model, os.path.join(MODELS_DIR, 'anomaly_model.pkl'))
    logger.info("Trained and saved Anomaly Detection Model.")
    
    return features

def predict_and_update_db(df, features):
    """Load models, predict on current data, and update database."""
    churn_model = joblib.load(os.path.join(MODELS_DIR, 'churn_model.pkl'))
    clv_model = joblib.load(os.path.join(MODELS_DIR, 'clv_model.pkl'))
    anomaly_model = joblib.load(os.path.join(MODELS_DIR, 'anomaly_model.pkl'))
    
    X = df[features]
    
    # Predictions
    df['predicted_churn_prob'] = churn_model.predict_proba(X)[:, 1]
    df['clv_forecast'] = clv_model.predict(X)
    # IsolationForest returns -1 for anomaly, 1 for normal
    df['is_anomaly'] = (anomaly_model.predict(X) == -1).astype(int)
    
    # Ensure columns exist in DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('ALTER TABLE customers ADD COLUMN predicted_churn_prob REAL')
        cursor.execute('ALTER TABLE customers ADD COLUMN clv_forecast REAL')
        cursor.execute('ALTER TABLE customers ADD COLUMN is_anomaly INTEGER')
    except sqlite3.OperationalError:
        pass # Columns already exist
        
    # Update DB
    for _, row in df.iterrows():
        cursor.execute('''
            UPDATE customers 
            SET predicted_churn_prob = ?, clv_forecast = ?, is_anomaly = ?
            WHERE customer_id = ?
        ''', (row['predicted_churn_prob'], row['clv_forecast'], row['is_anomaly'], row['customer_id']))
        
    conn.commit()
    conn.close()
    logger.info("Updated database with ML predictions.")

def run_ml_pipeline():
    logger.info("Starting ML Pipeline...")
    df = load_training_data()
    if df.empty:
        logger.warning("No data found for training.")
        return
        
    features = train_and_save_models(df)
    predict_and_update_db(df, features)
    logger.info("ML Pipeline completed successfully.")

if __name__ == "__main__":
    run_ml_pipeline()
