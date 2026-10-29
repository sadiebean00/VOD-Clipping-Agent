function ProjectDetailsPage ({project, onBack}) {
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
                    <h3>{project.title}</h3>
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
                <p>Platform: {project.platform}</p>
                <p>Status: {project.status}</p>
                <p>Created: {project.created}</p>
                <p>VOD URL: {project.url}</p>
            </div>

            <div className="panel">
                <h4>Generated Clips</h4>
                <p>No clips yet. Your clips will appear here once processing is built.</p>
            </div>
        </section>
    )
}

export default ProjectDetailsPage