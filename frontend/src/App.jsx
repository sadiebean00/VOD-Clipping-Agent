
import { useState, useEffect, cache } from 'react'
import './App.css'

// Main navigation items for the dashboard.
const navigationItems = [
  { name: 'Dashboard', icon: '⌂' },
  { name: 'New Project', icon: '+' },
  { name: 'My Projects', icon: '▤' },
  { name: 'Clips', icon: '▷' },
  { name: 'Settings', icon: '⚙' },
]

function NewProjectPage() {
  const [videoURL, setVideoURL] = useState('')
  const [status, setStatus] = useState('')
  async function handleLoadVOD() {
    if (videoURL.trim() === '') {
      setStatus('Please enter a video link first.')
      return
    }

    let url

    try {
      url = new URL(videoURL.trim())
    } catch {
      setStatus('That link does not look like a valid URL.')
      return
    }

    if (
      url.hostname !== 'youtube.com' &&
      url.hostname !== 'www.youtube.com' &&
      url.hostname != 'youtu.be' &&
      url.hostname != 'twitch.tv' &&
      url.hostname != 'www.twitch.tv'
    ) {
      setStatus('Please enter a YouTube or Twitch link.')
      return
    }
    
    setStatus('Sending link to backend...')

    try {
      const response = await fetch('http://127.0.0.1:8000/api/vod', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({url: videoURL.trim()}),
      })

    const data = await response.json()
    
    if (!response.ok) {
      setStatus(data.detail || data.message || 'The backend returned an error.')
      return
    }

    setStatus(`${data.message} Platform: ${data.platform}`)
    } catch(error) {
      console.error('Error contacting backend:', error)
      setStatus('Could not contact the backend. Is it running?')
    }
  }

  return (
    <div>
      <h2>New Clipping Project</h2>
      <p>Bring in a gaming VOD and prepare it for automatic highlight detection.</p>
      <h3>Video Source</h3>
      <p>Choose a VOD to analyse for highlights.</p>
      <input
        type="url"
        placeholder="Paste a Twitch or YouTube link"
        value={videoURL}
        onChange={(event) => setVideoURL(event.target.value)}/>
      <button onClick={handleLoadVOD}>Load VOD </button>
      <p>{status}</p>
    </div>
  )
}

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
          <>
            <section className="welcome-section">
              <div>
                <p className="eyebrow">WELCOME TO YOUR WORKSPACE</p>
                <h3>Turn long streams into great moments.</h3>
                <p className="welcome-description">
                  Find highlights, generate captions and create clips
                  from your gaming VODs, all on your own PC.
                </p>
                <button
                  className="primary-button"
                  onClick={() => setActivePage('New Project')}
                >
                  <span>+</span> Start a new project
                </button>
              </div>
              <div className="welcome-decoration" aria-hidden="true">
                <div className="decoration-ring ring-one" />
                <div className="decoration-ring ring-two" />
                <div className="play-symbol">▶</div>
              </div>
            </section>

            <section className="stats-grid">
              <article className="stat-card">
                <span className="stat-icon purple">▤</span>
                <p>Projects</p>
                <h3>0</h3>
                <span className="stat-note">Your VOD projects</span>
              </article>

              <article className="stat-card">
                <span className="stat-icon pink">▷</span>
                <p>Clips created</p>
                <h3>0</h3>
                <span className="stat-note">Your saved highlights</span>
              </article>

              <article className="stat-card">
                <span className="stat-icon blue">✦</span>
                <p>AI status</p>
                <h3 className="status-heading">Not configured</h3>
                <span className="stat-note">Local models come later</span>
              </article>
            </section>

            <section className="bottom-grid">
              <article className="panel">
                <div className="panel-heading">
                  <div>
                    <h3>Recent projects</h3>
                    <p>Your latest clipping projects will appear here.</p>
                  </div>
                  <span className="panel-symbol">▤</span>
                </div>
                <div className="empty-state">
                  <div className="empty-icon">▷</div>
                  <h4>No projects yet</h4>
                  <p>
                    Start with a Twitch VOD or a local video file.
                  </p>
                  <button
                    className="secondary-button"
                    onClick={() => setActivePage('New Project')}
                  >
                    Create your first project
                  </button>
                </div>
              </article>

              <article className="panel system-panel">
                <div className="panel-heading">
                  <div>
                    <h3>System overview</h3>
                    <p>Your local workspace</p>
                  </div>
                  <span className="system-indicator" />
                </div>
                <div className="system-row">
                  <span>Application</span>
                  <span className="system-value">Running</span>
                </div>
                <div className="system-row">
                  <span>Processing</span>
                  <span className="system-value muted">Not started</span>
                </div>
                <div className="system-row">
                  <span>AI models</span>
                  <span className="system-value muted">Not installed</span>
                </div>
                <p className="system-footnote">
                  AI features will be set up in later steps.
                </p>
              </article>
            </section>
          </>
        ) : (
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
