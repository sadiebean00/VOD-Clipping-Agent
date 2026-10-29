function DashboardPage({onNewProject}) {
    return (
        <>
            <section className="welcome-section">
                <div>
                    <p className="eyebrow">WELCOME TO YOUR WORKSPACE</p>
                    <h3>Turn your long streams into great moments.</h3>
                    <p className="welcome-description">
                        Find highlights, generate captions and create clips
                        from your gaming VODs, all on your own PC.
                    </p>
                    <button
                        className="primary-button"
                        onClick={onNewProject}
                    >
                        <span>+</span>Start a new project
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
                    <span className="stat-note">Your saved highlights & clips</span>
                </article>

                <article className="stat-card">
                    <span className="stat-icon blue">✦</span>
                    <p>AI status</p>
                    <h3 className="status-heading">Not Configured</h3>
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
                        <p>Start with a Twitch VOD or YouTube video.</p>
                        <button
                            className="secondary-button"
                            onClick={onNewProject}
                        >
                            Create your first project
                            </button>
                    </div>
                </article>

                <article className="panel system-panel">
                    <div className="panel-heading">
                        <div>
                            <h3>System Overview</h3>
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
                        <span className="system-value muted">Not Started</span>
                    </div>
                    <div className="system-row">
                        <span>AI Models</span>
                        <span className="system-value muted">Not Installed</span>
                    </div>

                    <p className="system-footnote">
                        AI features will be setup later.
                    </p>
                </article>
            </section>
        </>
    )
}

export default DashboardPage