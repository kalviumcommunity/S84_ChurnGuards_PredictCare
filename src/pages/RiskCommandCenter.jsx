import { AlertTriangle, TrendingUp, Clock, DollarSign } from 'lucide-react'

export default function RiskCommandCenter() {
  const healthScores = [
    { label: 'Low Risk', value: 142, color: '#10b981' },
    { label: 'Medium', value: 34, color: '#f59e0b' },
    { label: 'Critical', value: 12, color: '#dc2626' },
  ]

  const highRiskAccounts = [
    { name: 'Acme Corp', risk: 'Critical', revenue: '$3.2M', activity: '2 days ago', score: 89 },
    { name: 'Stark Industries', risk: 'High Alert', revenue: '$4.5M', activity: '5 days ago', score: 78 },
    { name: 'Wayne Ent.', risk: 'High', revenue: '$800K', activity: '1 week ago', score: 72 },
  ]

  const alerts = [
    { 
      type: 'critical',
      title: 'Acme Corp risk score jumped to 89',
      description: 'Support escalation + negative sentiment',
      time: '2 mins ago'
    },
    { 
      type: 'warning',
      title: 'Key sponsor at TechFlow departed',
      description: 'Executive team change detected',
      time: '30 mins ago'
    },
    { 
      type: 'info',
      title: 'Global Inc. renewal delayed',
      description: 'Expected contract renewal delayed by procurement',
      time: '1hr ago'
    },
  ]

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Risk Command Center</h1>
          <p style={styles.subtitle}>Tactical workspace for Customer Success Managers</p>
        </div>
        <button style={styles.exportBtn}>Export</button>
      </div>

      <div style={styles.summaryGrid}>
        <div style={styles.summaryCard}>
          <div style={styles.summaryLabel}>Health Score Summary</div>
          <div style={styles.healthGrid}>
            {healthScores.map((item, i) => (
              <div key={i} style={styles.healthItem}>
                <div style={styles.healthValue}>{item.value}</div>
                <div style={styles.healthLabel}>
                  <span style={{ ...styles.healthDot, background: item.color }}></span>
                  {item.label}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div style={styles.alertsCard}>
          <div style={styles.alertsHeader}>
            <AlertTriangle size={18} color="#dc2626" />
            <span style={styles.alertsTitle}>Active Risk Alerts</span>
            <span style={styles.alertsBadge}>Live Feed</span>
          </div>
          
          <div style={styles.alertsList}>
            {alerts.map((alert, i) => (
              <div key={i} style={styles.alertItem}>
                <div style={{
                  ...styles.alertIndicator,
                  background: alert.type === 'critical' ? '#dc2626' : 
                             alert.type === 'warning' ? '#f59e0b' : '#3b82f6'
                }}></div>
                <div style={styles.alertContent}>
                  <div style={styles.alertTitle}>{alert.title}</div>
                  <div style={styles.alertDesc}>{alert.description}</div>
                  <div style={styles.alertTime}>{alert.time}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={styles.accountsSection}>
        <div style={styles.accountsHeader}>
          <h2 style={styles.sectionTitle}>High Risk Accounts</h2>
          <div style={styles.filterGroup}>
            <button style={styles.filterBtn}>Filter by CSM</button>
            <button style={styles.filterBtn}>Actions</button>
          </div>
        </div>

        <table style={styles.table}>
          <thead>
            <tr style={styles.tableHeader}>
              <th style={styles.th}>Account Name</th>
              <th style={styles.th}>Risk Level</th>
              <th style={styles.th}>Revenue (ARR)</th>
              <th style={styles.th}>Last Activity</th>
              <th style={styles.th}>Score</th>
              <th style={styles.th}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {highRiskAccounts.map((account, i) => (
              <tr key={i} style={styles.tableRow}>
                <td style={styles.td}>
                  <div style={styles.accountName}>{account.name}</div>
                </td>
                <td style={styles.td}>
                  <span style={styles.riskBadge}>{account.risk}</span>
                </td>
                <td style={styles.td}>{account.revenue}</td>
                <td style={styles.td}>
                  <span style={styles.activityText}>{account.activity}</span>
                </td>
                <td style={styles.td}>
                  <div style={styles.scoreContainer}>
                    <div style={styles.scoreCircle}>{account.score}</div>
                  </div>
                </td>
                <td style={styles.td}>
                  <button style={styles.viewBtn}>View Details</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

const styles = {
  container: {
    maxWidth: 1400,
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 32,
  },
  title: {
    fontSize: 28,
    fontWeight: 600,
    color: '#e5e7eb',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: '#9ca3af',
  },
  exportBtn: {
    padding: '10px 20px',
    background: '#1e2936',
    border: '1px solid #3b82f6',
    borderRadius: 8,
    color: '#3b82f6',
    fontSize: 14,
    fontWeight: 500,
    cursor: 'pointer',
  },
  summaryGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: 24,
    marginBottom: 32,
  },
  summaryCard: {
    background: '#0f1419',
    border: '1px solid #1e2936',
    borderRadius: 12,
    padding: 24,
  },
  summaryLabel: {
    fontSize: 14,
    color: '#9ca3af',
    marginBottom: 20,
    fontWeight: 500,
  },
  healthGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: 16,
  },
  healthItem: {
    textAlign: 'center',
  },
  healthValue: {
    fontSize: 36,
    fontWeight: 700,
    color: '#e5e7eb',
    marginBottom: 8,
  },
  healthLabel: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    fontSize: 13,
    color: '#9ca3af',
  },
  healthDot: {
    width: 8,
    height: 8,
    borderRadius: '50%',
  },
  alertsCard: {
    background: '#0f1419',
    border: '1px solid #1e2936',
    borderRadius: 12,
    padding: 24,
  },
  alertsHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    marginBottom: 20,
  },
  alertsTitle: {
    fontSize: 14,
    fontWeight: 600,
    color: '#e5e7eb',
  },
  alertsBadge: {
    marginLeft: 'auto',
    padding: '4px 12px',
    background: '#1e2936',
    borderRadius: 6,
    fontSize: 12,
    color: '#10b981',
    fontWeight: 500,
  },
  alertsList: {
    display: 'flex',
    flexDirection: 'column',
    gap: 16,
  },
  alertItem: {
    display: 'flex',
    gap: 12,
    padding: 12,
    background: '#1e2936',
    borderRadius: 8,
  },
  alertIndicator: {
    width: 4,
    borderRadius: 2,
  },
  alertContent: {
    flex: 1,
  },
  alertTitle: {
    fontSize: 14,
    fontWeight: 500,
    color: '#e5e7eb',
    marginBottom: 4,
  },
  alertDesc: {
    fontSize: 13,
    color: '#9ca3af',
    marginBottom: 4,
  },
  alertTime: {
    fontSize: 12,
    color: '#6b7280',
  },
  accountsSection: {
    background: '#0f1419',
    border: '1px solid #1e2936',
    borderRadius: 12,
    padding: 24,
  },
  accountsHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 600,
    color: '#e5e7eb',
  },
  filterGroup: {
    display: 'flex',
    gap: 12,
  },
  filterBtn: {
    padding: '8px 16px',
    background: '#1e2936',
    border: '1px solid #374151',
    borderRadius: 6,
    color: '#9ca3af',
    fontSize: 13,
    cursor: 'pointer',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  tableHeader: {
    borderBottom: '1px solid #1e2936',
  },
  th: {
    padding: '12px 16px',
    textAlign: 'left',
    fontSize: 13,
    fontWeight: 600,
    color: '#9ca3af',
  },
  tableRow: {
    borderBottom: '1px solid #1e2936',
  },
  td: {
    padding: '16px',
    fontSize: 14,
    color: '#e5e7eb',
  },
  accountName: {
    fontWeight: 500,
  },
  riskBadge: {
    display: 'inline-block',
    padding: '4px 12px',
    background: '#7f1d1d',
    color: '#fca5a5',
    borderRadius: 6,
    fontSize: 12,
    fontWeight: 500,
  },
  activityText: {
    color: '#9ca3af',
  },
  scoreContainer: {
    display: 'flex',
    alignItems: 'center',
  },
  scoreCircle: {
    width: 48,
    height: 48,
    borderRadius: '50%',
    background: '#1e2936',
    border: '2px solid #dc2626',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 16,
    fontWeight: 700,
    color: '#dc2626',
  },
  viewBtn: {
    padding: '8px 16px',
    background: '#1e2936',
    border: '1px solid #3b82f6',
    borderRadius: 6,
    color: '#3b82f6',
    fontSize: 13,
    fontWeight: 500,
    cursor: 'pointer',
  },
}
