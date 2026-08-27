import CameraFrame from '../components/CameraFrame.jsx'
import DetectionTable from '../components/DetectionTable.jsx'
import FrameInspector from '../components/FrameInspector.jsx'
import MetricsPanel from '../components/MetricsPanel.jsx'
import SceneViewer from '../components/SceneViewer.jsx'
import TrackTimeline from '../components/TrackTimeline.jsx'

export default function ReplayPage({ frame, frames, detections, tracks, metrics, frameIndex, setFrameIndex }) {
  return (
    <main className="replay-grid">
      <section className="camera-region">
        <CameraFrame frame={frame} detections={detections} />
      </section>
      <section className="scene-region">
        <SceneViewer frame={frame} detections={detections} tracks={tracks} />
      </section>
      <aside className="inspector-region">
        <FrameInspector frames={frames} frameIndex={frameIndex} setFrameIndex={setFrameIndex} metrics={metrics} />
        <MetricsPanel metrics={metrics} frameId={frame?.id} />
      </aside>
      <section className="timeline-region">
        <TrackTimeline tracks={tracks} frameId={frame?.id} frameCount={frames.length} />
      </section>
      <section className="table-region">
        <DetectionTable detections={detections} />
      </section>
    </main>
  )
}
