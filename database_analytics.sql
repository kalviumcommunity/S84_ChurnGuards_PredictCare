-- ChurnGuard AI - Advanced Analytics Schema
-- Purpose: Time-series analysis, predictive metrics, and aggregation tables
-- Created: 2026-08-05

-- ============================================
-- CHURN PREDICTIONS TABLE
-- Stores ML model predictions and confidence scores
-- ============================================
CREATE TABLE IF NOT EXISTS churn_predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    prediction_date DATE NOT NULL,
    churn_probability DECIMAL(5, 4) CHECK(churn_probability BETWEEN 0 AND 1),
    risk_factors TEXT, -- JSON array of contributing factors
    confidence_score DECIMAL(5, 4),
    model_version VARCHAR(50),
    predicted_churn_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    UNIQUE(customer_id, prediction_date)
);

-- ============================================
-- CUSTOMER HEALTH HISTORY
-- Tracks health score changes over time
-- ============================================
CREATE TABLE IF NOT EXISTS customer_health_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    snapshot_date DATE NOT NULL,
    risk_score INTEGER,
    health_status VARCHAR(20),
    arr DECIMAL(12, 2),
    active_users INTEGER,
    open_tickets INTEGER,
    critical_tickets INTEGER,
    sentiment_score DECIMAL(3, 2), -- -1 to 1 scale
    engagement_score DECIMAL(5, 2), -- 0-100
    product_usage_score DECIMAL(5, 2), -- 0-100
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    UNIQUE(customer_id, snapshot_date)
);

-- ============================================
-- INTERVENTION ACTIONS
-- Tracks retention efforts and outcomes
-- ============================================
CREATE TABLE IF NOT EXISTS intervention_actions (
    action_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    action_type VARCHAR(100) CHECK(action_type IN (
        'Executive Call', 'Account Review', 'Discount Offer', 
        'Training Session', 'Feature Demo', 'Strategic Planning',
        'Escalation', 'Custom Solution', 'Service Credit'
    )),
    initiated_by VARCHAR(100),
    initiated_date DATE NOT NULL,
    completed_date DATE,
    status VARCHAR(50) CHECK(status IN ('Planned', 'In Progress', 'Completed', 'Cancelled')),
    outcome VARCHAR(50) CHECK(outcome IN ('Successful', 'Unsuccessful', 'Pending', 'N/A')),
    cost_estimate DECIMAL(10, 2),
    risk_score_before INTEGER,
    risk_score_after INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================
-- NPS SURVEYS
-- Net Promoter Score tracking
-- ============================================
CREATE TABLE IF NOT EXISTS nps_surveys (
    survey_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    stakeholder_id INTEGER,
    survey_date DATE NOT NULL,
    nps_score INTEGER CHECK(nps_score BETWEEN 0 AND 10),
    nps_category VARCHAR(20) CHECK(nps_category IN ('Detractor', 'Passive', 'Promoter')),
    feedback_text TEXT,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (stakeholder_id) REFERENCES stakeholders(stakeholder_id)
);

-- ============================================
-- REVENUE EVENTS
-- Track expansion, contraction, churn events
-- ============================================
CREATE TABLE IF NOT EXISTS revenue_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    event_date DATE NOT NULL,
    event_type VARCHAR(50) CHECK(event_type IN (
        'New Customer', 'Expansion', 'Contraction', 
        'Renewal', 'Churn', 'Reactivation', 'Upgrade', 'Downgrade'
    )),
    previous_arr DECIMAL(12, 2),
    new_arr DECIMAL(12, 2),
    arr_change DECIMAL(12, 2),
    reason TEXT,
    recorded_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================
-- FEATURE ADOPTION
-- Track feature usage and adoption rates
-- ============================================
CREATE TABLE IF NOT EXISTS feature_adoption (
    adoption_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    feature_name VARCHAR(100) NOT NULL,
    first_used_date DATE,
    last_used_date DATE,
    usage_count INTEGER DEFAULT 0,
    adoption_status VARCHAR(50) CHECK(adoption_status IN (
        'Not Adopted', 'Exploring', 'Adopted', 'Power User', 'Abandoned'
    )),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    UNIQUE(customer_id, feature_name)
);

-- ============================================
-- CONTRACT DETAILS
-- Detailed contract and renewal information
-- ============================================
CREATE TABLE IF NOT EXISTS contracts (
    contract_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    contract_number VARCHAR(100) UNIQUE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    contract_value DECIMAL(12, 2) NOT NULL,
    billing_frequency VARCHAR(50) CHECK(billing_frequency IN (
        'Monthly', 'Quarterly', 'Annually', 'Custom'
    )),
    auto_renewal BOOLEAN DEFAULT TRUE,
    payment_terms VARCHAR(100),
    contract_status VARCHAR(50) CHECK(contract_status IN (
        'Active', 'Expiring Soon', 'Expired', 'Renewed', 'Cancelled'
    )),
    signed_date DATE,
    cancellation_date DATE,
    cancellation_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================
-- ESCALATION HISTORY
-- Track escalation paths and resolutions
-- ============================================
CREATE TABLE IF NOT EXISTS escalations (
    escalation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id VARCHAR(50),
    customer_id INTEGER NOT NULL,
    escalation_level INTEGER CHECK(escalation_level BETWEEN 1 AND 5),
    escalated_from VARCHAR(100),
    escalated_to VARCHAR(100),
    escalation_reason TEXT NOT NULL,
    escalated_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    resolution_notes TEXT,
    status VARCHAR(50) CHECK(status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================
-- COMPETITIVE INTELLIGENCE
-- Track competitor mentions and win/loss data
-- ============================================
CREATE TABLE IF NOT EXISTS competitive_intel (
    intel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    competitor_name VARCHAR(100),
    intel_type VARCHAR(50) CHECK(intel_type IN (
        'Evaluation', 'Migration Risk', 'Feature Comparison', 
        'Pricing Concern', 'Lost Deal', 'Won Deal'
    )),
    intel_date DATE NOT NULL,
    details TEXT,
    risk_level VARCHAR(20) CHECK(risk_level IN ('Low', 'Medium', 'High', 'Critical')),
    action_taken TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================
-- INDEXES FOR ANALYTICS PERFORMANCE
-- ============================================
CREATE INDEX IF NOT EXISTS idx_churn_predictions_customer ON churn_predictions(customer_id, prediction_date DESC);
CREATE INDEX IF NOT EXISTS idx_health_history_customer ON customer_health_history(customer_id, snapshot_date DESC);
CREATE INDEX IF NOT EXISTS idx_interventions_customer ON intervention_actions(customer_id, initiated_date DESC);
CREATE INDEX IF NOT EXISTS idx_nps_customer_date ON nps_surveys(customer_id, survey_date DESC);
CREATE INDEX IF NOT EXISTS idx_revenue_events_date ON revenue_events(customer_id, event_date DESC);
CREATE INDEX IF NOT EXISTS idx_feature_adoption_customer ON feature_adoption(customer_id, adoption_status);
CREATE INDEX IF NOT EXISTS idx_contracts_customer ON contracts(customer_id, contract_status);
CREATE INDEX IF NOT EXISTS idx_escalations_customer ON escalations(customer_id, status);

-- ============================================
-- ADVANCED ANALYTICAL VIEWS
-- ============================================

-- Customer Lifetime Value (LTV) Calculation
CREATE VIEW IF NOT EXISTS vw_customer_ltv AS
SELECT 
    c.customer_id,
    c.company_name,
    c.arr,
    c.tenure_months,
    ROUND(c.arr * (c.tenure_months / 12.0), 2) as lifetime_value,
    ROUND(c.arr * (c.tenure_months / 12.0) * (1 - c.risk_score / 100.0), 2) as risk_adjusted_ltv,
    COUNT(DISTINCT re.event_id) as revenue_events_count,
    SUM(CASE WHEN re.event_type = 'Expansion' THEN re.arr_change ELSE 0 END) as total_expansion,
    SUM(CASE WHEN re.event_type = 'Contraction' THEN re.arr_change ELSE 0 END) as total_contraction
FROM customers c
LEFT JOIN revenue_events re ON c.customer_id = re.customer_id
GROUP BY c.customer_id, c.company_name, c.arr, c.tenure_months, c.risk_score;

-- Churn Risk Trend (30-day rolling)
CREATE VIEW IF NOT EXISTS vw_churn_risk_trends AS
SELECT 
    customer_id,
    snapshot_date,
    risk_score,
    AVG(risk_score) OVER (
        PARTITION BY customer_id 
        ORDER BY snapshot_date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as risk_score_30d_avg,
    health_status,
    sentiment_score,
    engagement_score,
    product_usage_score
FROM customer_health_history
ORDER BY customer_id, snapshot_date DESC;

-- Intervention Effectiveness
CREATE VIEW IF NOT EXISTS vw_intervention_effectiveness AS
SELECT 
    action_type,
    COUNT(*) as total_actions,
    SUM(CASE WHEN outcome = 'Successful' THEN 1 ELSE 0 END) as successful_count,
    ROUND(AVG(CASE WHEN outcome = 'Successful' THEN 1.0 ELSE 0.0 END) * 100, 2) as success_rate,
    ROUND(AVG(risk_score_before - risk_score_after), 2) as avg_risk_reduction,
    ROUND(AVG(cost_estimate), 2) as avg_cost,
    COUNT(DISTINCT customer_id) as customers_affected
FROM intervention_actions
WHERE status = 'Completed' AND outcome != 'Pending'
GROUP BY action_type
ORDER BY success_rate DESC;

-- NPS Trend by Customer
CREATE VIEW IF NOT EXISTS vw_nps_trends AS
SELECT 
    c.customer_id,
    c.company_name,
    COUNT(n.survey_id) as survey_count,
    ROUND(AVG(n.nps_score), 2) as avg_nps_score,
    MAX(n.survey_date) as last_survey_date,
    SUM(CASE WHEN n.nps_category = 'Promoter' THEN 1 ELSE 0 END) as promoter_count,
    SUM(CASE WHEN n.nps_category = 'Detractor' THEN 1 ELSE 0 END) as detractor_count,
    ROUND((SUM(CASE WHEN n.nps_category = 'Promoter' THEN 1.0 ELSE 0.0 END) - 
           SUM(CASE WHEN n.nps_category = 'Detractor' THEN 1.0 ELSE 0.0 END)) / 
           COUNT(n.survey_id) * 100, 2) as nps_score_calculated
FROM customers c
LEFT JOIN nps_surveys n ON c.customer_id = n.customer_id
GROUP BY c.customer_id, c.company_name;

-- Feature Adoption Summary
CREATE VIEW IF NOT EXISTS vw_feature_adoption_summary AS
SELECT 
    feature_name,
    COUNT(DISTINCT customer_id) as total_customers,
    SUM(CASE WHEN adoption_status IN ('Adopted', 'Power User') THEN 1 ELSE 0 END) as adopted_count,
    ROUND(AVG(CASE WHEN adoption_status IN ('Adopted', 'Power User') THEN 1.0 ELSE 0.0 END) * 100, 2) as adoption_rate,
    SUM(usage_count) as total_usage,
    ROUND(AVG(usage_count), 2) as avg_usage_per_customer
FROM feature_adoption
GROUP BY feature_name
ORDER BY adoption_rate DESC;

-- At-Risk Revenue Pipeline
CREATE VIEW IF NOT EXISTS vw_at_risk_revenue AS
SELECT 
    c.customer_id,
    c.company_name,
    c.arr,
    c.risk_score,
    c.health_status,
    c.renewal_date,
    CAST(julianday(c.renewal_date) - julianday('now') AS INTEGER) as days_to_renewal,
    CASE 
        WHEN c.risk_score >= 80 THEN 'Very High'
        WHEN c.risk_score >= 60 THEN 'High'
        WHEN c.risk_score >= 40 THEN 'Medium'
        ELSE 'Low'
    END as churn_probability,
    COUNT(DISTINCT t.ticket_id) as open_critical_tickets,
    MAX(n.nps_score) as latest_nps,
    i.action_count
FROM customers c
LEFT JOIN tickets t ON c.customer_id = t.customer_id 
    AND t.status NOT IN ('Resolved', 'Closed') 
    AND t.priority = 'Critical'
LEFT JOIN nps_surveys n ON c.customer_id = n.customer_id
LEFT JOIN (
    SELECT customer_id, COUNT(*) as action_count
    FROM intervention_actions
    WHERE status IN ('Planned', 'In Progress')
    GROUP BY customer_id
) i ON c.customer_id = i.customer_id
WHERE c.risk_score >= 60
GROUP BY c.customer_id, c.company_name, c.arr, c.risk_score, c.health_status, c.renewal_date
ORDER BY c.risk_score DESC, c.arr DESC;

-- Escalation Response Time Analysis
CREATE VIEW IF NOT EXISTS vw_escalation_metrics AS
SELECT 
    c.company_name,
    e.escalation_level,
    e.status,
    COUNT(*) as escalation_count,
    ROUND(AVG(
        CASE 
            WHEN e.resolved_at IS NOT NULL 
            THEN (julianday(e.resolved_at) - julianday(e.escalated_at)) * 24 
            ELSE NULL 
        END
    ), 2) as avg_resolution_hours,
    MIN(e.escalated_at) as first_escalation,
    MAX(e.escalated_at) as latest_escalation
FROM escalations e
JOIN customers c ON e.customer_id = c.customer_id
GROUP BY c.company_name, e.escalation_level, e.status
ORDER BY c.company_name, e.escalation_level;
