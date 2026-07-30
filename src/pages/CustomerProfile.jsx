import { Building2, Mail, Phone, Calendar, TrendingDown, AlertCircle, CheckCircle, MessageSquare } from 'lucide-react'

export default function CustomerProfile() {
  const company = {
    name: 'GlobalTech Inc.',
    status: 'At-Risk / High Value',
    industry: 'Enterprise SaaS',
    plan: 'Enterprise Premium',
    arr: '$3.2M',
    contract: 'Annual',
    renewal: 'Dec 15, 2026',
    csm: 'Sarah Mitchell',
    phone: '+1 (415) 234-5678',
    email: 'contact@globaltech.com',
  }

  const metrics = [
    { label: 'Health Score', value: '72', status: 'declining', color: '#f59e0b' },
    { label: 'Support Tickets', value: '24', subtext: '6 last 7 days', color: '#dc2626' },
    { label: 'Last Login', value: '14', subtext: 'days ago', color: '#dc2626' },
    { label: 'Sentiment', value: 'Negative', color: '#dc2626' },
  ]

  const timeline = [
    {
      type: 'escalation',
      title: 'Active Escalation',
      desc: 'Key sponsor has frozen budget. Procurement delay.',
      time: '2 days ago',
      icon: AlertCircle,
      color: '#dc2626',
    },
    {
      type: 'ticket',
      title: 'Support Ticket Resolved',
      desc: 'Dashboard Q3 export issue - resolved with workaround',
      time: '5 days ago',
      icon: CheckCircle,
      color: '#10b981',
    },
    {
      type: 'message',
      title: 'CSM Check-in Email',
      desc: 'Outreach sent regarding upcoming renewal & product adoption',
      time: '1 week ago',
      icon: MessageSquare,
      color: '#3b82f6',
    },
    {
      type: 'ticket',
      title: 'Complaint Logged',
      desc: 'Customer dissatisfied with response time on critical API issue',
      time: '2 weeks ago',
      icon: AlertCircle,
      color: '#f59e0b',
    },
  ]

  const recommendations = [
    'Schedule executive check-in to address budget concerns',
    'Offer extended trial of premium features',
    'Fast-track pending support tickets',
    'Provide dedicated technical account manager',
  ]

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div style={styles.companyHeader}>
          <div style={styles.companyIcon}>
            <Building2 size={32} color="#3b82f6" />
          </div>
          <div>
            <h1 style={styles.companyName}>{company.name}</h1>
            <span style={styles.statusBadge}>{company.status}</span>
          </div>
        </div>
        <button style={styles.actionBtn}>Schedule Intervention</button>
      </div>

      <div style={styles.grid}>
        <div style={styles.mainColumn}>
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Customer Profile</h2>
            <div style={styles.profileGrid}>
              <div style={styles.profileItem}>
                <span style={styles.profileLabel}>Industry</span>
                <span style={styles.profileValue}>{company.industry}</span>
              </div>
              <div style={styles.profileItem}>
                <span style={styles.profileLabel}>Plan Type</span>
                <span style={styles.profileValue}>{company.plan}</span>
              </div>
              <div style={styles.profileItem}>
                <span style={styles.profileLabel}>ARR</span>
                <span style={styles.profileValue}>{company.arr}</span>
              </div>
              <div style={styles.profileItem}>
                <span style={styles.profileLabel}>Contract</span>
                <span style={styles.profileValue}>{company.contract}</span>
              </div>
              <div style={styles.profileItem}>
                <span style={styles.profileLabel}>Renewal Date</span>
                <span style={styles.profileValue}>{company.renewal}</span>
              </div>
              <div style={styles.profileItem}>
                <span style={styles.profileLabel}>CSM</span>
                <span style={styles.profileValue}>{company.csm}</span>
              </div>
            </div>

            <div style={styles.contactSection}>
              <h3 style={styles.sectionSubtitle}>Contact Info</h3>
              <div style={styles.contactGrid}>
                <div style={styles.contactItem}>
                  <Phone size={16} color="#9ca3af" />
                  <span>{company.phone}</span>
                </div>
                <div style={styles.contactItem}>
                  <Mail size={16} color="#9ca3af" />
                  <span>{company.email}</span>
                </div>
              </div>
            </div>
          </div>

          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Customer Timeline</h2>
            <div style={styles.timeline}>
              {timeline.map((item, i) => (
                <div key={i} style={styles.timelineItem}>
                  <div style={{ ...styles.timelineIcon, background: item.color }}>
                    <item.icon size={16} color="#fff" />
                  </div>
                  <div style={styles.timelineContent}>
                    <div style={styles.timelineTitle}>{item.title}</div>
                    <div style={styles.timelineDesc}>{item.desc}</div>
                    <div style={styles.timelineTime}>{item.time}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div style={styles.sidebar}>
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Key Metrics</h2>
            <div style={styles.metricsGrid}>
              {metrics.map((metric, i) => (
                <div key={i} style={styles.metricCard}>
                  <div style={styles.metricLabel}>{metric.label}</div>
                  <div style={{ ...styles.metricValue, color: metric.color }}>
                    {metric.value}
                  </div>
                  {metric.subtext && (
                    <div style={styles.metricSubtext}>{metric.subtext}</div>
                  )}
                </div>
              ))}
            </div>
          </div>

          <div style={styles.card}>
            <div style={styles.alertBox}>
              <AlertCircle size={20} color="#dc2626" />
              <div>
                <div style={styles.alertTitle}>Active Escalation</div>
                <div style={styles.alertText}>
                  Key sponsor has frozen budget. Procurement delay.
                </div>
              </div>
            </div>
          </div>

          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Retention Recommendations</h2>
            <div style={styles.recList}>
              {recommendations.map((rec, i) => (
                <div key={i} style={styles.recItem}>
                  <div style={styles.recBullet}>{i + 1}</div>
                  <div style={styles.recText}>{rec}</div>
                </div>
              ))}
            </div>
          </div>
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
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 32,
  },
  companyHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: 20,
  },
  companyIcon: {
    width: 72,
    height: 72,
    background: '#0f1419',
    border: '1px solid #1e2936',
    borderRadius: 12,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  companyName: {
    fontSize: 28,
    fontWeight: 600,
    color: '#e5e7eb',
    marginBottom: 8,
  },
  statusBadge: {
    display: 'inline-block',
    padding: '6px 16px',
    background: '#7f1d1d',
    color: '#fca5a5',
    borderRadius: 6,
    fontSize: 13,
    fontWeight: 500,
  },
  actionBtn: {
    padding: '12px 24px',
    background: '#dc2626',
    border: 'none',
    borderRadius: 8,
    color: '#fff',
    fontSize: 14,
    fontWeight: 600,
    cursor: 'pointer',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '2fr 1fr',
    gap: 24,
  },
  mainColumn: {
    display: 'flex',
    flexDirection: 'column',
    gap: 24,
  },
  sidebar: {
    display: 'flex',
    flexDirection: 'column',
    gap: 24,
  },
  card: {
    background: '#0f1419',
    border: '1px solid #1e2936',
    borderRadius: 12,
    padding: 24,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: 600,
    color: '#e5e7eb',
    marginBottom: 20,
  },
  profileGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap: 20,
    marginBottom: 24,
  },
  profileItem: {
    display: 'flex',
    flexDirection: 'column',
    gap: 6,
  },
  profileLabel: {
    fontSize: 13,
    color: '#9ca3af',
    fontWeight: 500,
  },
  profileValue: {
    fontSize: 15,
    color: '#e5e7eb',
    fontWeight: 500,
  },
  contactSection: {
    paddingTop: 24,
    borderTop: '1px solid #1e2936',
  },
  sectionSubtitle: {
    fontSize: 14,
    fontWeight: 600,
    color: '#e5e7eb',
    marginBottom: 16,
  },
  contactGrid: {
    display: 'flex',
    flexDirection: 'column',
    gap: 12,
  },
  contactItem: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    fontSize: 14,
    color: '#e5e7eb',
  },
  timeline: {
    display: 'flex',
    flexDirection: 'column',
    gap: 20,
  },
  timelineItem: {
    display: 'flex',
    gap: 16,
  },
  timelineIcon: {
    width: 36,
    height: 36,
    borderRadius: 8,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  timelineContent: {
    flex: 1,
  },
  timelineTitle: {
    fontSize: 14,
    fontWeight: 600,
    color: '#e5e7eb',
    marginBottom: 4,
  },
  timelineDesc: {
    fontSize: 13,
    color: '#9ca3af',
    marginBottom: 4,
    lineHeight: 1.5,
  },
  timelineTime: {
    fontSize: 12,
    color: '#6b7280',
  },
  metricsGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: 16,
  },
  metricCard: {
    padding: 16,
    background: '#1e2936',
    borderRadius: 8,
  },
  metricLabel: {
    fontSize: 12,
    color: '#9ca3af',
    marginBottom: 8,
    fontWeight: 500,
  },
  metricValue: {
    fontSize: 24,
    fontWeight: 700,
    marginBottom: 4,
  },
  metricSubtext: {
    fontSize: 11,
    color: '#6b7280',
  },
  alertBox: {
    display: 'flex',
    gap: 12,
    padding: 16,
    background: '#7f1d1d',
    borderRadius: 8,
  },
  alertTitle: {
    fontSize: 14,
    fontWeight: 600,
    color: '#fca5a5',
    marginBottom: 4,
  },
  alertText: {
    fontSize: 13,
    color: '#fecaca',
    lineHeight: 1.5,
  },
  recList: {
    display: 'flex',
    flexDirection: 'column',
    gap: 14,
  },
  recItem: {
    display: 'flex',
    gap: 12,
    alignItems: 'flex-start',
  },
  recBullet: {
    width: 24,
    height: 24,
    borderRadius: '50%',
    background: '#3b82f6',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 12,
    fontWeight: 700,
    flexShrink: 0,
  },
  recText: {
    fontSize: 13,
    color: '#e5e7eb',
    lineHeight: 1.6,
    paddingTop: 2,
  },
}
