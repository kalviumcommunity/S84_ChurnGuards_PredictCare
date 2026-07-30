import { TrendingUp, TrendingDown, DollarSign, Users, AlertCircle } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

export default function ExecutiveDashboard() {
  const kpiData = [
    { label: 'Projected Churn Rate', value: '12.4%', change: '+2.1%', trend: 'up', color: '#dc2626' },
    { label: 'Revenue at Risk', value: '$4.2M', change: '-8%', trend: 'down', color: '#10b981' },
    { label: 'Prevention Actions', value: '68', change: '+15.8%', trend: 'up', color: '#3b82f6' },
  ]

  const churnTrendData = [
    { month: 'Jan', actual: 85, prevented: 15 },
    { month: 'Feb', actual: 78, prevented: 22 },
    { month: 'Mar', actual: 82, prevented: 18 },
    { month: 'Apr', actual: 75, prevented: 25 },
    { month: 'May', actual: 70, prevented: 30 },
    { month: 'Jun', actual: 65, prevented: 35 },
  ]

  const segmentData = [
    { name: 'Enterprise High-Risk', value: 35, color: '#dc2626' },
    { name: 'Mid-Market', value: 28, color: '#f59e0b' },
    { name: 'SMB', value: 37, color: '#10b981' },
  ]

  const reasonsData = [
    { reason: 'Product Dissatisfaction', value: 45 },
    { reason: 'Price Objection', value: 32 },
    { reason: 'Lack of Engagement', value: 23 },
  ]

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Executive Insights</h1>
        <p style={styles.subtitle}>Real-time view of customer retention and churn performance</p>
      </div>

      <div style={styles.kpiGrid}>
        {kpiData.map((kpi, i) => (
          <div key={i} style={styles.kpiCard}>
            <div style={styles.kpiHeader}>
              <span style={styles.kpiLabel}>{kpi.label}</span>
              <span style={{ ...styles.kpiChange, color: kpi.trend === 'up' ? '#dc2626' : '#10b981' }}>
                {kpi.change}
              </span>
            </div>
            <div style={styles.kpiValue}>{kpi.value}</div>
            <div style={styles.kpiFooter}>Last 30-day trend</div>
          </div>
        ))}
      </div>

      <div style={styles.grid}>
        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <h3 style={styles.cardTitle}>Churn Trend vs. Prevention Actions</h3>
            <div style={styles.legend}>
              <span style={styles.legendItem}>
                <span style={{ ...styles.legendDot, background: '#1e293b' }}></span>
                Actual Churn
              </span>
              <span style={styles.legendItem}>
                <span style={{ ...styles.legendDot, background: '#e5e7eb' }}></span>
                Prevented by Actions
              </span>
            </div>
          </div>
          <div style={styles.chartContainer}>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={churnTrendData}>
                <XAxis dataKey="month" stroke="#4b5563" />
                <YAxis stroke="#4b5563" />
                <Bar dataKey="actual" stackId="a" fill="#1e293b" radius={[0, 0, 4, 4]} />
                <Bar dataKey="prevented" stackId="a" fill="#e5e7eb" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div style={styles.card}>
          <h3 style={styles.cardTitle}>Risk Distribution by Segment</h3>
          <div style={styles.chartContainer}>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={segmentData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  dataKey="value"
                >
                  {segmentData.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div style={styles.pieLabels}>
            {segmentData.map((item, i) => (
              <div key={i} style={styles.pieLabel}>
                <span style={{ ...styles.legendDot, background: item.color }}></span>
                <span>{item.name}</span>
                <span style={styles.pieLabelValue}>{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={styles.card}>
        <h3 style={styles.cardTitle}>Top Reasons for Dissatisfaction</h3>
        <div style={styles.reasonsList}>
          {reasonsData.map((item, i) => (
            <div key={i} style={styles.reasonItem}>
              <div style={styles.reasonLabel}>{item.reason}</div>
              <div style={styles.reasonBar}>
                <div style={{ ...styles.reasonBarFill, width: `${item.value}%` }}></div>
              </div>
              <div style={styles.reasonValue}>{item.value}%</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    maxWidth: 1400,
  },
  header: {
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
  kpiGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: 24,
    marginBottom: 32,
  },
  kpiCard: {
    background: '#0f1419',
    border: '1px solid #1e2936',
    borderRadius: 12,
    padding: 24,
  },
  kpiHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  kpiLabel: {
    fontSize: 13,
    color: '#9ca3af',
    fontWeight: 500,
  },
  kpiChange: {
    fontSize: 13,
    fontWeight: 600,
  },
  kpiValue: {
    fontSize: 36,
    fontWeight: 700,
    color: '#e5e7eb',
    marginBottom: 8,
  },
  kpiFooter: {
    fontSize: 12,
    color: '#6b7280',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: 24,
    marginBottom: 24,
  },
  card: {
    background: '#0f1419',
    border: '1px solid #1e2936',
    borderRadius: 12,
    padding: 24,
  },
  cardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: 600,
    color: '#e5e7eb',
    marginBottom: 20,
  },
  legend: {
    display: 'flex',
    gap: 20,
  },
  legendItem: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    fontSize: 13,
    color: '#9ca3af',
  },
  legendDot: {
    width: 12,
    height: 12,
    borderRadius: 3,
  },
  chartContainer: {
    width: '100%',
  },
  pieLabels: {
    display: 'flex',
    flexDirection: 'column',
    gap: 12,
    marginTop: 20,
  },
  pieLabel: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
    fontSize: 14,
    color: '#e5e7eb',
  },
  pieLabelValue: {
    marginLeft: 'auto',
    fontWeight: 600,
  },
  reasonsList: {
    display: 'flex',
    flexDirection: 'column',
    gap: 20,
  },
  reasonItem: {
    display: 'grid',
    gridTemplateColumns: '1fr 2fr auto',
    gap: 16,
    alignItems: 'center',
  },
  reasonLabel: {
    fontSize: 14,
    color: '#e5e7eb',
  },
  reasonBar: {
    height: 8,
    background: '#1e2936',
    borderRadius: 4,
    overflow: 'hidden',
  },
  reasonBarFill: {
    height: '100%',
    background: '#3b82f6',
    borderRadius: 4,
  },
  reasonValue: {
    fontSize: 14,
    fontWeight: 600,
    color: '#e5e7eb',
    minWidth: 45,
    textAlign: 'right',
  },
}
