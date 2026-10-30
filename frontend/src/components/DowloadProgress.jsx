function DownloadProgress({ progress = 0}) {
    const percentage = Math.min(100, Math.max(0, progress))

    return (
        <div className="download-progress">
            <div className="download-progress-heading">
                <span>Downloading your VOD</span>
                <span>{Math.round(percentage)}%</span>
            </div>

            <div className="download-progress-track">
                <div
                    className="download-progress-fill"
                    style={{ width: `${percentage}%`}}
                />    
            </div>
        </div>
    )
}

export default DownloadProgress