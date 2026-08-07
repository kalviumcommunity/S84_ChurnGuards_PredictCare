-- Data Snapshot Tables for Version History
-- Allows users to view historical data uploads

-- ============================================
-- Table: data_snapshots
-- Tracks each data upload with metadata
-- ============================================
CREATE TABLE IF NOT EXISTS data_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_name VARCHAR(255) NOT NULL,
    snapshot_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_count INTEGER,
    ticket_count INTEGER,
    interaction_count INTEGER,
    uploaded_by VARCHAR(100),
    notes TEXT,
    is_active BOOLEAN DEFAULT 0
);

-- ============================================
-- Table: customers_history
-- Stores historical customer data
-- ============================================
CREATE TABLE IF NOT EXISTS customers_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER NOT NULL,
    customer_id INTEGER,
    company_name VARCHAR(255),
    industry VARCHAR(100),
    company_size VARCHAR(50),
    arr DECIMAL(12, 2),
    risk_score INTEGER,
    health_status VARCHAR(20),
    sentiment VARCHAR(20),
    tenure_months INTEGER,
    renewal_date DATE,
    last_activity TIMESTAMP,
    created_at TIMESTAMP,
    FOREIGN KEY (snapshot_id) REFERENCES data_snapshots(snapshot_id)
);

-- ============================================
-- Table: tickets_history
-- Stores historical ticket data
-- ============================================
CREATE TABLE IF NOT EXISTS tickets_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER NOT NULL,
    ticket_id VARCHAR(50),
    customer_id INTEGER,
    subject TEXT,
    description TEXT,
    priority VARCHAR(20),
    status VARCHAR(50),
    category VARCHAR(100),
    sentiment VARCHAR(20),
    assigned_to VARCHAR(100),
    created_at TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (snapshot_id) REFERENCES data_snapshots(snapshot_id)
);

-- ============================================
-- Table: interactions_history
-- Stores historical interaction data
-- ============================================
CREATE TABLE IF NOT EXISTS interactions_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER NOT NULL,
    interaction_id INTEGER,
    customer_id INTEGER,
    interaction_type VARCHAR(50),
    interaction_date TIMESTAMP,
    duration_minutes INTEGER,
    sentiment VARCHAR(20),
    notes TEXT,
    outcome VARCHAR(100),
    FOREIGN KEY (snapshot_id) REFERENCES data_snapshots(snapshot_id)
);

-- ============================================
-- Indexes for fast snapshot retrieval
-- ============================================
CREATE INDEX IF NOT EXISTS idx_customers_history_snapshot ON customers_history(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_tickets_history_snapshot ON tickets_history(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_interactions_history_snapshot ON interactions_history(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_date ON data_snapshots(snapshot_date DESC);
CREATE INDEX IF NOT EXISTS idx_snapshots_active ON data_snapshots(is_active);

-- ============================================
-- View: v_snapshot_summary
-- Quick overview of all snapshots
-- ============================================
CREATE VIEW IF NOT EXISTS v_snapshot_summary AS
SELECT 
    s.snapshot_id,
    s.snapshot_name,
    s.snapshot_date,
    s.customer_count,
    s.ticket_count,
    s.interaction_count,
    s.uploaded_by,
    s.is_active,
    CASE 
        WHEN s.is_active = 1 THEN 'Active'
        ELSE 'Archived'
    END as status
FROM data_snapshots s
ORDER BY s.snapshot_date DESC;
