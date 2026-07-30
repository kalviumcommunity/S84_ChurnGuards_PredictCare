import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import ExecutiveDashboard from './pages/ExecutiveDashboard'
import RiskCommandCenter from './pages/RiskCommandCenter'
import SupportWorkspace from './pages/SupportWorkspace'
import CustomerProfile from './pages/CustomerProfile'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<ExecutiveDashboard />} />
          <Route path="/risk-center" element={<RiskCommandCenter />} />
          <Route path="/support" element={<SupportWorkspace />} />
          <Route path="/customer/:id" element={<CustomerProfile />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
