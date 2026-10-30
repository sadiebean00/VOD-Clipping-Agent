import { useEffect, useState } from "react"
import DownloadProgress from "../components/DownloadProgress"

function ProjectDetailsPage ({project, onBack}) {
    const [latestProject, setLatestProject] = useState(project)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [refreshCount, setRefreshCount] = useState(0)
    const [clips, setClips]= useState([])
    const [clipsError, setClipsError] = useState('')

    useEffect(() => {
        async function loadProject() {
            try {
                const response = await fetch(
                    `http://192.168.0.31:8000/api/projects/${project.id}`,
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
    }, [project?.id, refreshCount])

    useEffect(() => {
        async function loadClips() {
            try{
                const response = await fetch(
                    `http://192.168.0.31:8000/api/projects/${project.id}/clips`,
                    { cache: 'no-store' }
                )

                if (!response.ok) {
                    throw new Error('Could not load generated clips.')
                }

                const data = await response.json()
                setClips(data.clips)
                setClipsError('')
            } catch (error) {
                setClipsError(error.message)
            }
        }
        
        if (project?.id) {
            loadClips()
        }
    }, [project?.id, refreshCount])

    useEffect(() => {
        const interval = setInterval(() => {
            setRefreshCount((count) => count + 1)
        }, 3000)

        return () => clearInterval(interval)
    }, [])

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
                <h4>Download Progress</h4>

                {latestProject.status === 'downloading' ? (
                    <DownloadProgress progress={latestProject.download_progress} />
                ) : latestProject.status === 'downloaded' ? (
                    <DownloadProgress progress={100} />
                ) : (
                    <p>{latestProject.processing_message}</p>
                )}
            </div>

            <div className="panel">
                <h4>Project Information</h4>
                <p>Platform: {latestProject.platform}</p>
                <p>Status: {latestProject.status}</p>
                <p>Processing: {latestProject.processing_message}</p>
                <p>
                    Created: {new Date(latestProject.created_at).toLocaleString('en-GB', {
                        day: 'numeric',
                        month: 'long',
                        year: 'numeric',
                        hour: '2-digit',
                    minute: '2-digit'
                    })}
                </p>
                <p>VOD URL: {latestProject.url}</p>
            </div>

            <div className="panel">
                <h4>Generated Clips</h4>

                {clipsError && <p role="alert">{clipsError}</p>}

                {!clipsError && clips.length == 0 && (
                    <p>No clips generated yet. Create a project to get started.</p>
                )}

                {clips.map((clip, index) => (
                    <article className="panel" key={clip.filename}>
                        <h4>Clip {index + 1}</h4>

                        <video
                            controls
                            width="100%"
                            src={`http://192.168.0.31:8000/api/projects/${project.id}/clips/${encodeURIComponent(clip.filename)}`}
                        />

                        <a
                            href={`http://192.168.0.31:8000/api/projects/${project.id}/clips/${encodeURIComponent(clip.filename)}`}
                            download={clip.filename}
                        >
                            Download MP4
                        </a>

                        <p>Filename: {clip.filename}</p>
                        <p>File size: {(clip.size_bytes / (1024 * 1024)).toFixed(2)} MB</p>
                    </article>
                ))}
            </div>
        </section>
    )
}

export default ProjectDetailsPage