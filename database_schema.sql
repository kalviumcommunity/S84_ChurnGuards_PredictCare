-- ChurnGuard AI Database Schema
-- Purpose: Store customer, ticket, and interaction data for churn prediction
-- Created: 2026-08-05

-- ============================================
-- Table: customers
-- Stores customer account information
-- ============================================
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    company_size VARCHAR(50),
    arr DECIMAL(12, 2) NOT NULL,
    risk_score INTEGER CHECK(risk_score BETWEEN 0 AND 100),
    health_status VARCHAR(20) CHECK(health_status IN ('Low Risk', 'Medium', 'Critical')),
    sentiment VARCHAR(20) CHECK(sentiment IN ('Positive', 'Neutral', 'Negative')),
    tenure_months INTEGER,
    renewal_date DATE,
    last_activity TIMESTAMP,
    predicted_churn_prob DECIMAL(5, 4),
    clv_forecast DECIMAL(12, 2),
    is_anomaly BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Table: tickets
-- Stores support ticket information
-- ============================================
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id VARCHAR(50) PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    description TEXT,
    priority VARCHAR(20) CHECK(priority IN ('Low', 'Medium', 'High', 'Critical')),
    status VARCHAR(50) CHECK(status IN ('Open', 'In Progress', 'Awaiting Response', 'Resolved', 'Closed')),
    category VARCHAR(100),
    risk_score INTEGER CHECK(risk_score BETWEEN 0 AND 100),
    sentiment VARCHAR(20) CHECK(sentiment IN ('Positive', 'Neutral', 'Negative')),
    assigned_to VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================
-- Table: interactions
-- Stores customer interaction history
-- ============================================
CREATE TABLE IF NOT EXISTS interactions (
    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    interaction_type VARCHAR(50) CHECK(interaction_type IN ('Call', 'Email', 'Meeting', 'QBR', 'Training', 'Survey')),
    interaction_date TIMESTAMP NOT NULL,
    duration_minutes INTEGER,
    sentiment VARCHAR(20) CHECK(sentiment IN ('Positive', 'Neutral', 'Negative')),
    notes TEXT,
    outcome VARCHAR(100),
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================
-- Table: usage_metrics
-- Stores product usage metrics
-- ============================================
CREATE TABLE IF NOT EXISTS usage_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    metric_date DATE NOT NULL,
    active_users INTEGER DEFAULT 0,
    logins INTEGER DEFAULT 0,
    feature_usage_score DECIMAL(5, 2),
    api_calls INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    session_duration_avg INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    UNIQUE(customer_id, metric_date)
);

-- ============================================
-- Table: risk_alerts
-- Stores automated risk alerts
-- ============================================
CREATE TABLE IF NOT EXISTS risk_alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) CHECK(severity IN ('Low', 'Medium', 'High', 'Critical')),
    message TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    resolved_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================
-- Table: stakeholders
-- Stores key stakeholder information
-- ============================================
CREATE TABLE IF NOT EXISTS stakeholders (
    stakeholder_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    role VARCHAR(100),
    department VARCHAR(100),
    influence_level VARCHAR(20) CHECK(influence_level IN ('Low', 'Medium', 'High', 'Champion')),
    last_contact_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================
-- Indexes for Performance
-- ============================================
CREATE INDEX IF NOT EXISTS idx_customers_risk ON customers(risk_score, health_status);
CREATE INDEX IF NOT EXISTS idx_customers_renewal ON customers(renewal_date);
CREATE INDEX IF NOT EXISTS idx_tickets_customer ON tickets(customer_id);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status, priority);
CREATE INDEX IF NOT EXISTS idx_interactions_customer ON interactions(customer_id, interaction_date);
CREATE INDEX IF NOT EXISTS idx_usage_customer_date ON usage_metrics(customer_id, metric_date);
CREATE INDEX IF NOT EXISTS idx_alerts_customer ON risk_alerts(customer_id, is_resolved);

-- ============================================
-- Views for Common Queries
-- ============================================

-- View: High-risk customers with open tickets
CREATE VIEW IF NOT EXISTS vw_high_risk_customers AS
SELECT 
    c.customer_id,
    c.company_name,
    c.risk_score,
    c.arr,
    c.health_status,
    c.renewal_date,
    COUNT(DISTINCT t.ticket_id) as open_tickets,
    SUM(CASE WHEN t.priority = 'Critical' THEN 1 ELSE 0 END) as critical_tickets
FROM customers c
LEFT JOIN tickets t ON c.customer_id = t.customer_id AND t.status NOT IN ('Resolved', 'Closed')
WHERE c.health_status IN ('Critical', 'Medium')
GROUP BY c.customer_id, c.company_name, c.risk_score, c.arr, c.health_status, c.renewal_date;

-- View: Customer engagement summary
CREATE VIEW IF NOT EXISTS vw_customer_engagement AS
SELECT 
    c.customer_id,
    c.company_name,
    c.risk_score,
    COUNT(DISTINCT i.interaction_id) as total_interactions,
    MAX(i.interaction_date) as last_interaction,
    AVG(CASE WHEN i.sentiment = 'Positive' THEN 3 
             WHEN i.sentiment = 'Neutral' THEN 2 
             ELSE 1 END) as avg_sentiment_score
FROM customers c
LEFT JOIN interactions i ON c.customer_id = i.customer_id
GROUP BY c.customer_id, c.company_name, c.risk_score;

-- View: Weekly usage trends
CREATE VIEW IF NOT EXISTS vw_weekly_usage_trends AS
SELECT 
    customer_id,
    strftime('%Y-W%W', metric_date) as week,
    AVG(active_users) as avg_active_users,
    AVG(feature_usage_score) as avg_feature_usage,
    SUM(api_calls) as total_api_calls,
    SUM(errors_count) as total_errors
FROM usage_metrics
GROUP BY customer_id, strftime('%Y-W%W', metric_date);

-- PR 11: Feature Completeness Indexes
CREATE INDEX IF NOT EXISTS idx_customers_health_status ON customers(health_status);
CREATE INDEX IF NOT EXISTS idx_customers_risk_score ON customers(risk_score);
