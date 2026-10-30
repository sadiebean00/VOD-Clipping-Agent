
import { useState } from 'react'

function NewProjectPage({onProjectCreated}) {
  const [videoURL, setVideoURL] = useState('')
  const [projectTitle, setProjectTitle] = useState('')
  const [status, setStatus] = useState('')

  async function handleLoadVOD() {
    if (projectTitle.trim() === '') {
      setStatus('Please enter a project name.')
      return
    }

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
      url.protocol !== 'https:' ||
      ![
        'youtube.com',
        'www.youtube.com',
        'm.youtube.com',
        'youtu.be',
        'twitch.tv',
        'www.twitch.tv',
        'm.twitch.tv',
      ].includes(url.hostname)
    ) {
      setStatus('Please enter a valid HTTPS YouTube or Twitch link.')
      return
    }

    setStatus('Sending project to backend...')

    try {
      const response = await fetch(
        'http://192.168.0.31:8000/api/vod',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            url: videoURL.trim(),
            title: projectTitle.trim(),
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        setStatus(
          data.detail || data.message || 'The backend returned an error.'
        )
        return
      }

      onProjectCreated(data.project_id)
    } catch (error) {
      console.error('Error contacting backend:', error)
      setStatus('Could not contact the backend. Is it running?')
    }
  }

  return (
    <div>
      <h2>New Clipping Project</h2>
      <p>
        Bring in a gaming VOD and prepare it for automatic highlight detection.
      </p>

      <h3>Video Source</h3>
      <p>Choose a VOD to analyse for highlights.</p>

      <input
        type="text"
        placeholder="Enter a project name"
        value={projectTitle}
        onChange={(event) => setProjectTitle(event.target.value)}
      />

      <input
        type="url"
        placeholder="Paste a Twitch or YouTube link"
        value={videoURL}
        onChange={(event) => setVideoURL(event.target.value)}
      />

      <button onClick={handleLoadVOD}>Load VOD</button>
      <p role="status">{status}</p>
    </div>
  )
}

export default NewProjectPage
