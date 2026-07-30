import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, AlertTriangle, Headphones, Users, Settings, Bell } from 'lucide-react'

export default function Layout({ children }) {
  const location = useLocation()
  
  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Executive Dashboard' },
    { path: '/risk-center', icon: AlertTriangle, label: 'Risk Command Center' },
    { path: '/support', icon: Headphones, label: 'Support Workspace' },
    { path: '/customer/1', icon: Users, label: 'Customer Directory' },
  ]

  return (
    <div style={styles.container}>
      <aside style={styles.sidebar}>
        <div style={styles.logo}>
          <div style={styles.logoIcon}>CG</div>
          <span style={styles.logoText}>ChurnGuard AI</span>
        </div>
        
        <nav style={styles.nav}>
          {navItems.map(item => (
            <Link
              key={item.path}
              to={item.path}
              style={{
                ...styles.navItem,
                ...(location.pathname === item.path ? styles.navItemActive : {})
              }}
            >
              <item.icon size={20} />
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>

        <div style={styles.sidebarFooter}>
          <button style={styles.footerBtn}>
            <Settings size={20} />
            Settings
          </button>
        </div>
      </aside>

      <div style={styles.main}>
        <header style={styles.header}>
          <div style={styles.headerLeft}>
            <h1 style={styles.headerTitle}>Churn Prevention System</h1>
          </div>
          <div style={styles.headerRight}>
            <button style={styles.iconBtn}>
              <Bell size={20} />
            </button>
            <div style={styles.userProfile}>
              <div style={styles.avatar}>PM</div>
              <span>Product Manager</span>
            </div>
          </div>
        </header>
        
        <main style={styles.content}>
          {children}
        </main>
      </div>
    </div>
  )
}

const styles = {
  container: {
    display: 'flex',
    minHeight: '100vh',
    background: '#0a0e1a',
  },
  sidebar: {
    width: 280,
    background: '#0f1419',
    borderRight: '1px solid #1e2936',
    display: 'flex',
    flexDirection: 'column',
    padding: '24px 16px',
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
    marginBottom: 32,
    padding: '0 8px',
  },
  logoIcon: {
    width: 40,
    height: 40,
    background: 'linear-gradient(135deg, #3b82f6 0%, #1e40af 100%)',
    borderRadius: 8,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 700,
    fontSize: 16,
  },
  logoText: {
    fontSize: 18,
    fontWeight: 600,
    color: '#e5e7eb',
  },
  nav: {
    display: 'flex',
    flexDirection: 'column',
    gap: 4,
    flex: 1,
  },
  navItem: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
    padding: '12px 16px',
    borderRadius: 8,
    color: '#9ca3af',
    textDecoration: 'none',
    fontSize: 14,
    fontWeight: 500,
    transition: 'all 0.2s',
    cursor: 'pointer',
  },
  navItemActive: {
    background: '#1e2936',
    color: '#3b82f6',
  },
  sidebarFooter: {
    paddingTop: 16,
    borderTop: '1px solid #1e2936',
  },
  footerBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
    padding: '12px 16px',
    background: 'transparent',
    border: 'none',
    borderRadius: 8,
    color: '#9ca3af',
    fontSize: 14,
    fontWeight: 500,
    cursor: 'pointer',
    width: '100%',
  },
  main: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    height: 64,
    background: '#0f1419',
    borderBottom: '1px solid #1e2936',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0 32px',
  },
  headerLeft: {},
  headerTitle: {
    fontSize: 18,
    fontWeight: 600,
    color: '#e5e7eb',
  },
  headerRight: {
    display: 'flex',
    alignItems: 'center',
    gap: 16,
  },
  iconBtn: {
    width: 40,
    height: 40,
    background: 'transparent',
    border: '1px solid #1e2936',
    borderRadius: 8,
    color: '#9ca3af',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
  },
  userProfile: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
    fontSize: 14,
  },
  avatar: {
    width: 36,
    height: 36,
    borderRadius: 8,
    background: '#3b82f6',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 600,
    fontSize: 13,
  },
  content: {
    flex: 1,
    padding: 32,
    overflowY: 'auto',
  },
}
