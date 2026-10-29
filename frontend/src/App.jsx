
import { useState, useEffect } from 'react'
import NewProjectPage from './pages/NewProjectPage'
import DashboardPage from './pages/DashboardPage'
import MyProjectsPage from './pages/MyProjectsPage'
import './App.css'

// Main navigation items for the dashboard.
const navigationItems = [
  { name: 'Dashboard', icon: '⌂' },
  { name: 'New Project', icon: '+' },
  { name: 'My Projects', icon: '▤' },
  { name: 'Clips', icon: '▷' },
  { name: 'Settings', icon: '⚙' },
]

function App() {
  // Remember which navigation item is selected.
  const [activePage, setActivePage] = useState('Dashboard')
  const [backendStatus, setBackendStatus] = useState('checking')

  useEffect(() => {
    async function checkBackend() {
      try {
        const response = await fetch(
          'http://127.0.0.1:8000/api/health',
          {cache: 'no-store'}
        )

        if (!response.ok) {
          throw new Error('Backend unavailable')
        }
        
        setBackendStatus('online')
      } catch {
        setBackendStatus('offline')
      }
    }

    checkBackend()

    const intervalID = setInterval(checkBackend, 5000)

    return () => clearInterval(intervalID)
  }, [])

  return (
    <div className="app-shell">
      {/* Sidebar navigation */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">V</div>
          <div>
            <h1>VOD Studio</h1>
            <p>CLIPPING AGENT</p>
          </div>
        </div>

        <p className="sidebar-label">WORKSPACE</p>

        <nav className="navigation">
          {navigationItems.map((item) => (
            <button
              key={item.name}
              className={`nav-item ${
                activePage === item.name ? 'active' : ''
              }`}
              onClick={() => setActivePage(item.name)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.name}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <span className="status-dot" />
          <div>
            <p>Local AI</p>
            <span>Ready to configure</span>
          </div>
        </div>
      </aside>

      {/* Main dashboard content */}
      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">YOUR CREATOR WORKSPACE</p>
            <h2>{activePage}</h2>
          </div>
          <div className="profile-badge">VC</div>
        </header>

        <div className={`backend-status ${backendStatus}`}>
          <span className="status-dot" />
          Backend: {backendStatus}
          </div>

        {activePage === 'New Project' ? (
          <NewProjectPage/>
        )  
        : activePage === 'Dashboard' ? (
          <DashboardPage
            onNewProject={() => setActivePage('New Project')}
          /> 
        ) 
        : activePage === 'My Projects' ? (
            <MyProjectsPage
             onNewProject={() => setActivePage('New Project')} />
        ) :     
        (
          <section className="placeholder-panel">
            <div className="empty-icon">✦</div>
            <h3>{activePage}</h3>
            <p>
              This section is part of the dashboard layout.
              We'll build its features in a later step.
            </p>
            <button
              className="secondary-button"
              onClick={() => setActivePage('Dashboard')}
            >
              Back to dashboard
            </button>
          </section>
        )}

        <footer className="app-footer">
          VOD Studio · Local-first gaming VOD tools
        </footer>
      </main>
    </div>
  )
}

export default App
