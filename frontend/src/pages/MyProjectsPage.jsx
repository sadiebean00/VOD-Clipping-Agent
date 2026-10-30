import { useEffect, useState } from "react"

function MyProjectsPage({onNewProject, onOpenProject}) {
    const [projects, setProjects] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [refreshing, setRefreshing] = useState(false)
    const [cleaning, setCleaning] = useState(false)

     async function loadProjects() {
        if (projects.length === 0) {
            setLoading(true)
        }
        setError('')

        try {
            const response = await fetch(
                'http://127.0.0.1:8000/api/projects',
                { cache: 'no-store'}
            )

            if (!response.ok) {
                throw new Error('Could not load projects.')
            }

            const data = await response.json()
            setProjects(currentProjects => {
                if (JSON.stringify(currentProjects) === JSON.stringify(data)) {
                    return currentProjects
                }

                return data
            })
            } catch {
                setError('Could not load projects. Is the backend running?')
            } finally {
                setLoading(false)
            }
        }

         async function handleRefresh() {
                setRefreshing(true)

                try {
                    await loadProjects()
                } finally {
                setRefreshing(false)
                }
            }

            async function handleRemove(projectID) {
                const confirmed = window.confirm(
                    'Are you sure you want to permanently delete this project?'
                )

                if (!confirmed) {
                    return
                }

                try {
                    const response = await fetch(
                        `http://127.0.0.1:8000/api/projects/${projectID}`,
                        {method: 'DELETE'}
                    )

                    if (!response.ok) {
                        throw new Error('Could not delete the project.')
                    }

                    await loadProjects()
                } catch (error) {
                    setError(error.message)
                }
            }

            async function handleCleanUp() {
                const confirmed = window.confirm(
                    "Are you sure you want to permanently delete ALL projects, downloaded VODs and generated clips? This cannot be undone."
                )

                if (!confirmed) {
                    return
                }

                setCleaning(true)

                try {
                    const response = await fetch(
                        'http://127.0.0.1:8000/api/projects',
                        { method: 'DELETE'}
                    )

                    if (!response.ok) {
                        throw new Error('Could not clean up project data.')
                    }

                    await loadProjects()
                } catch (error) {
                    setError(error.message)
                } finally {
                    setCleaning(false)
                }
            }

        useEffect(() => {
            loadProjects()

            const interval = setInterval(() => {
                loadProjects()
            }, 3000)

            return () => clearInterval(interval)
    }, [])

    return (
        <section className="placeholder-panel">
            <div className="panel-heading">
                <div>
                    <h3>MyProjects</h3>
                    <p>Your saved VOD clipping projects.</p>
                    <button
                        className="primary-button"
                        onClick={onNewProject}
                    >
                        + Create a New Project
                        </button>
                </div>

                <button
                    className="secondary-button"
                    onClick={handleRefresh}
                    disabled={refreshing || loading}
                >
                    {refreshing ? 'Refreshing...' : 'Refresh Projects'}
                </button>

                <button
                    className="secondary-button"
                    onClick={handleCleanUp}
                    disabled={cleaning || loading}
                >
                    {cleaning ? 'Cleaning Up...' : 'Clean Up Data'}
                </button>
            </div>
            {loading && <p>Loading projects...</p>}

            {error && <p role="alert">{error}</p>}

            {!loading && !error && projects.length === 0 && (
                <p>No projects yet. Create a new project to get started.</p>
            )}

            {!loading && !error && projects.length > 0 && (
                <div>
                    {projects.map((project) => (
                        <article className="panel" key={project.id}>
                            <h4
                                className="clickable-project-title"
                                onClick={() => onOpenProject(project)}
                            >
                                {project.title}
                            </h4>
                            
                            <p>Platform: {project.platform}</p>
                            {(project.status === 'downloading' || project.status === 'downloaded') && (
                                <p>
                                    Download Progress: {
                                        project.status === 'downloaded'
                                            ? 100
                                            : Math.round(project.download_progress || 0)
                                    }%
                                </p>
)}

                            <p>
                                Status: {
                                    project.status === 'downloaded'
                                        ? 'Download Complete'
                                        : project.status === 'downloading'
                                        ? 'Downloading...'
                                        : project.status === 'failed'
                                        ? 'Download Failed'
                                        : project.status === 'pending'
                                        ? 'Waiting to Download'
                                        : project.status
                                }
                            </p>
                            <p>
                                Created: {new Date(project.created_at).toLocaleString('en-GB', {
                                    day: 'numeric',
                                    month: 'long',
                                    year: 'numeric',
                                    hour: '2-digit',
                                    minute: '2-digit'
                                })}
                            </p>
                            
                            <button
                                className="primary-button"
                                onClick={() => onOpenProject(project)}
                            >
                                Open Project
                            </button>
                            
                            <button
                                className="secondary-button"
                                onClick={() => handleRemove(project.id)}
                            >
                                Remove Project
                            </button>
                        </article>
                    ))}
                </div>
            )}
        </section>
    )
}

export default MyProjectsPage