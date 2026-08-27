import { useEffect, useState } from 'react'
import Home from './pages/Home.jsx'
import MetricsPage from './pages/MetricsPage.jsx'
import ReplayPage from './pages/ReplayPage.jsx'
import { fetchReplayBundle } from './api/client.js'

const tabs = [
  { id: 'replay', label: 'Replay' },
  { id: 'metrics', label: 'Metrics' },
  { id: 'home', label: 'Overview' },
]

export default function App() {
  const [activeTab, setActiveTab] = useState('replay')
  const [bundle, setBundle] = useState({ frames: [], detections: [], tracks: [], metrics: null })
  const [frameIndex, setFrameIndex] = useState(0)
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    fetchReplayBundle()
      .then((data) => {
        setBundle(data)
        setStatus('ready')
      })
      .catch(() => setStatus('offline'))
  }, [])

  const frame = bundle.frames[frameIndex] ?? null
  const frameDetections = frame ? bundle.detections.filter((item) => item.frame_id === frame.id) : []

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">PerceptionViz Replay</p>
          <h1>Driving-scene replay and perception validation</h1>
        </div>
        <nav className="tabbar" aria-label="Dashboard sections">
          {tabs.map((tab) => (
            <button key={tab.id} className={activeTab === tab.id ? 'active' : ''} onClick={() => setActiveTab(tab.id)}>
              {tab.label}
            </button>
          ))}
        </nav>
      </header>

      {status === 'offline' && (
        <div className="status-banner">Backend is not reachable. Start FastAPI on port 8000 or set VITE_API_BASE_URL.</div>
      )}

      {activeTab === 'replay' && (
        <ReplayPage
          frame={frame}
          frames={bundle.frames}
          detections={frameDetections}
          tracks={bundle.tracks}
          metrics={bundle.metrics}
          frameIndex={frameIndex}
          setFrameIndex={setFrameIndex}
        />
      )}
      {activeTab === 'metrics' && <MetricsPage metrics={bundle.metrics} detections={bundle.detections} tracks={bundle.tracks} />}
      {activeTab === 'home' && <Home metrics={bundle.metrics} status={status} />}
    </div>
  )
}
