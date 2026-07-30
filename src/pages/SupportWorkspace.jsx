import { Search, Filter, MessageSquare, Clock, User } from 'lucide-react'

export default function SupportWorkspace() {
  const tickets = [
    {
      id: '#TKT-2847',
      customer: 'Sarah Zhang',
      company: 'GlobalTech Inc.',
      subject: 'Data export failing on Q3 Reports Dashboard',
      priority: 'High',
      status: 'In Progress',
      riskScore: 72,
      sentiment: 'Negative',
      created: '2 days ago',
    },
    {
      id: '#TKT-2846',
      customer: 'Michael Chen',
      company: 'Acme Corp',
      subject: 'API rate limits blocking integration',
      priority: 'Critical',
      status: 'Open',
      riskScore: 89,
      sentiment: 'Negative',
      created: '3 hours ago',
    },
    {
      id: '#TKT-2845',
      customer: 'Emma Wilson',
      company: 'TechFlow',
      subject: 'Unable to add new team members',
      priority: 'Medium',
      status: 'Awaiting Response',
      riskScore: 45,
      sentiment: 'Neutral',
      created: '1 day ago',
    },
  ]

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Support Agent Workspace</h1>
          <p style={styles.subtitle}>Ticket management with Customer 360 context</p>
        </div>
        <button style={styles.newTicketBtn}>+ New Ticket</button>
      </div>

      <div style={styles.filtersBar}>
        <div style={styles.searchBox}>
          <Search size={18} color="#9ca3af" />
          <input 
            type="text" 
            placeholder="Search tickets, customers, or issues..." 
            style={styles.searchInput}
          />
        </div>
        <div style={styles.filterBtns}>
          <button style={styles.filterBtn}>
            <Filter size={16} />
            Filter by CSM
          </button>
          <button style={styles.filterBtn}>Priority</button>
          <button style={styles.filterBtn}>Status</button>
        </div>
      </div>

      <div style={styles.statsBar}>
        <div style={styles.statItem}>
          <span style={styles.statLabel}>Open Tickets:</span>
          <span style={styles.statValue}>58</span>
        </div>
        <div style={styles.statItem}>
          <span style={styles.statLabel}>Avg Response Time:</span>
          <span style={styles.statValue}>2.4 hrs</span>
        </div>
        <div style={styles.statItem}>
          <span style={styles.statLabel}>High Risk:</span>
          <span style={{ ...styles.statValue, color: '#dc2626' }}>12</span>
        </div>
      </div>

      <div style={styles.ticketsList}>
        {tickets.map((ticket, i) => (
          <div key={i} style={styles.ticketCard}>
            <div style={styles.ticketHeader}>
              <div style={styles.ticketLeft}>
                <span style={styles.ticketId}>{ticket.id}</span>
                <span style={{
                  ...styles.priorityBadge,
                  background: ticket.priority === 'Critical' ? '#7f1d1d' :
                             ticket.priority === 'High' ? '#7c2d12' : '#422006',
                  color: ticket.priority === 'Critical' ? '#fca5a5' :
                         ticket.priority === 'High' ? '#fdba74' : '#fcd34d',
                }}>
                  {ticket.priority}
                </span>
                <span style={styles.statusBadge}>{ticket.status}</span>
              </div>
              <div style={styles.ticketRight}>
                <span style={styles.timeText}>
                  <Clock size={14} />
                  {ticket.created}
                </span>
              </div>
            </div>

            <div style={styles.ticketBody}>
              <h3 style={styles.ticketSubject}>{ticket.subject}</h3>
              <div style={styles.customerInfo}>
                <User size={16} color="#9ca3af" />
                <span style={styles.customerName}>{ticket.customer}</span>
                <span style={styles.separator}>•</span>
                <span style={styles.companyName}>{ticket.company}</span>
              </div>
            </div>

            <div style={styles.ticketFooter}>
              <div style={styles.riskSection}>
                <span style={styles.riskLabel}>Risk Score:</span>
                <div style={{
                  ...styles.riskScore,
                  color: ticket.riskScore >= 70 ? '#dc2626' : 
                         ticket.riskScore >= 50 ? '#f59e0b' : '#10b981',
                  borderColor: ticket.riskScore >= 70 ? '#dc2626' : 
                               ticket.riskScore >= 50 ? '#f59e0b' : '#10b981',
                }}>
                  {ticket.riskScore}
                </div>
              </div>
              <div style={styles.sentimentSection}>
                <span style={styles.sentimentLabel}>Sentiment:</span>
                <span style={{
                  ...styles.sentimentValue,
                  color: ticket.sentiment === 'Negative' ? '#dc2626' : '#9ca3af',
                }}>
                  {ticket.sentiment}
                </span>
              </div>
              <button style={styles.viewDetailsBtn}>View Customer 360</button>
            </div>
          </div>
        ))}
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
    marginBottom: 24,
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
  newTicketBtn: {
    padding: '12px 24px',
    background: '#3b82f6',
    border: 'none',
    borderRadius: 8,
    color: '#fff',
    fontSize: 14,
    fontWeight: 600,
    cursor: 'pointer',
  },
  filtersBar: {
    display: 'flex',
    gap: 16,
    marginBottom: 24,
  },
  searchBox: {
    flex: 1,
    display: 'flex',
    alignItems: 'center',
    gap: 12,
    padding: '12px 16px',
    background: '#0f1419',
    border: '1px solid #1e2936',
    borderRadius: 8,
  },
  searchInput: {
    flex: 1,
    background: 'transparent',
    border: 'none',
    outline: 'none',
    color: '#e5e7eb',
    fontSize: 14,
  },
  filterBtns: {
    display: 'flex',
    gap: 12,
  },
  filterBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    padding: '12px 20px',
    background: '#0f1419',
    border: '1px solid #1e2936',
    borderRadius: 8,
    color: '#9ca3af',
    fontSize: 14,
    cursor: 'pointer',
  },
  statsBar: {
    display: 'flex',
    gap: 32,
    padding: '16px 24px',
    background: '#0f1419',
    border: '1px solid #1e2936',
    borderRadius: 8,
    marginBottom: 24,
  },
  statItem: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
  },
  statLabel: {
    fontSize: 14,
    color: '#9ca3af',
  },
  statValue: {
    fontSize: 16,
    fontWeight: 700,
    color: '#e5e7eb',
  },
  ticketsList: {
    display: 'flex',
    flexDirection: 'column',
    gap: 16,
  },
  ticketCard: {
    background: '#0f1419',
    border: '1px solid #1e2936',
    borderRadius: 12,
    padding: 20,
  },
  ticketHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  ticketLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
  },
  ticketId: {
    fontSize: 14,
    fontWeight: 600,
    color: '#3b82f6',
  },
  priorityBadge: {
    padding: '4px 12px',
    borderRadius: 6,
    fontSize: 12,
    fontWeight: 600,
  },
  statusBadge: {
    padding: '4px 12px',
    background: '#1e2936',
    borderRadius: 6,
    fontSize: 12,
    color: '#9ca3af',
    fontWeight: 500,
  },
  ticketRight: {},
  timeText: {
    display: 'flex',
    alignItems: 'center',
    gap: 6,
    fontSize: 13,
    color: '#6b7280',
  },
  ticketBody: {
    marginBottom: 16,
  },
  ticketSubject: {
    fontSize: 16,
    fontWeight: 600,
    color: '#e5e7eb',
    marginBottom: 12,
  },
  customerInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    fontSize: 14,
  },
  customerName: {
    color: '#e5e7eb',
    fontWeight: 500,
  },
  separator: {
    color: '#4b5563',
  },
  companyName: {
    color: '#9ca3af',
  },
  ticketFooter: {
    display: 'flex',
    alignItems: 'center',
    gap: 24,
    paddingTop: 16,
    borderTop: '1px solid #1e2936',
  },
  riskSection: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
  },
  riskLabel: {
    fontSize: 13,
    color: '#9ca3af',
  },
  riskScore: {
    width: 40,
    height: 40,
    borderRadius: '50%',
    border: '2px solid',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 14,
    fontWeight: 700,
  },
  sentimentSection: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
  },
  sentimentLabel: {
    fontSize: 13,
    color: '#9ca3af',
  },
  sentimentValue: {
    fontSize: 14,
    fontWeight: 600,
  },
  viewDetailsBtn: {
    marginLeft: 'auto',
    padding: '10px 20px',
    background: '#1e2936',
    border: '1px solid #3b82f6',
    borderRadius: 8,
    color: '#3b82f6',
    fontSize: 13,
    fontWeight: 600,
    cursor: 'pointer',
  },
}
