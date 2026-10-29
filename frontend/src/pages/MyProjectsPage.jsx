import { useEffect, useState } from "react"

function MyProjectsPage({onNewProject}) {
    const [projects, setProjects] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [refreshing, setRefreshing] = useState(false)

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
            setProjects(data)
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
                } catch(error) {
                    setError.Error(error.message)
                }
            }
        useEffect(() => {
            loadProjects()
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
                            <h4>{project.title}</h4>
                            <p>Platform: {project.platform}</p>
                            <p>Status: {project.status}</p>
                            <p>Created: {project.created_at}</p>

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