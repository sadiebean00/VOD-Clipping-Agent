import { useEffect, useState } from "react"

function ProjectDetailsPage ({project, onBack}) {
    const [latestProject, setLatestProject] = useState(project)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        async function loadProject() {
            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/api/projects/${project.id}`,
                    { cache: 'no-store'}
                )

                if (!response.ok) {
                    throw new Error ('Could not load project details.')
                }

                const data = await response.json()
                setLatestProject(data)
            } catch (error) {
                setError(error.message)
            } finally {
                setLoading(false)
            }
        }

        if (project?.id) {
            loadProject()
        }
    }, [project?.id])

    if (loading) {
        return (
            <section className="placeholder-panel">
                <p>Loading project details...</p>
            </section>
        )
    }

    if (error) {
        return (
            <section className="placeholder-panel">
                <p role="alert">{error}</p>
                <button
                    className="secondary-button"
                    onClick={onBack}
                >
                    Back to My Projects
                </button>
            </section>
        )
    }

    if(!project) {
        return (
            <section className="placeholder-panel">
                <h3>No project selected</h3>
                <button 
                    className="secondary-button"
                    onClick={onBack}
                >
                    Back to My Projects
                </button>
            </section>
        )
    }

    return (
        <section className="placeholder-panel">
            <div className="panel-heading">
                <div>
                    <h3>{latestProject.title}</h3>
                    <p>Project Details</p>
                </div>

                <button
                    className="secondary-button"
                    onClick={onBack}
                >
                    Back to My Projects
                </button>
            </div>

            <div className="panel">
                <h4>Project Information</h4>
                <p>Platform: {latestProject.platform}</p>
                <p>Status: {latestProject.status}</p>
                <p>Processing: {latestProject.processing_message}</p>
                <p>Created: {latestProject.created}</p>
                <p>VOD URL: {latestProject.url}</p>
            </div>

            <div className="panel">
                <h4>Generated Clips</h4>
                <p>No clips yet. Your clips will appear here once processing is built.</p>
            </div>
        </section>
    )
}

export default ProjectDetailsPage