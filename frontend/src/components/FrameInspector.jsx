import { useState } from 'react'
import { runInference } from '../api/client.js'

export default function FrameInspector({ frames, frameIndex, setFrameIndex, metrics }) {
  const [message, setMessage] = useState('')
  const frame = frames[frameIndex]

  async function handleRunInference() {
    if (!frame) return
    setMessage('running')
    try {
      const detections = await runInference(frame.id)
      setMessage(`${detections.length} detections returned`)
    } catch {
      setMessage('request failed')
    }
  }

  return (
    <section className="side-panel">
      <div className="panel-title"><span>Inspector</span><strong>{frames.length} frames</strong></div>
      <div className="frame-stepper">
        <button onClick={() => setFrameIndex(Math.max(0, frameIndex - 1))}>Prev</button>
        <input type="range" min="0" max={Math.max(0, frames.length - 1)} value={frameIndex} onChange={(event) => setFrameIndex(Number(event.target.value))} />
        <button onClick={() => setFrameIndex(Math.min(frames.length - 1, frameIndex + 1))}>Next</button>
      </div>
      <div className="frame-facts">
        <span>Timestamp {frame?.timestamp?.toFixed(2) ?? '-'}s</span>
        <span>Ground truth {frame?.ground_truth.length ?? 0}</span>
        <span>Recall {metrics?.frames.find((item) => item.frame_id === frame?.id)?.recall.toFixed(2) ?? '-'}</span>
      </div>
      <button className="primary-action" onClick={handleRunInference}>Run inference on this frame</button>
      {message && <p className="run-message">{message}</p>}
    </section>
  )
}
