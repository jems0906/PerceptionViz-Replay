export default function TrackTimeline({ tracks, frameId, frameCount }) {
  return (
    <div className="timeline-panel">
      <div className="panel-title"><span>Track timeline</span><strong>{tracks.length} IDs</strong></div>
      <div className="timeline-grid">
        {tracks.map((track) => (
          <div className="timeline-row" key={track.track_id}>
            <span className="track-label">T{track.track_id}</span>
            <div className="timeline-cells">
              {Array.from({ length: frameCount }).map((_, index) => {
                const currentFrame = index + 1
                const active = track.points.some((point) => point.frame_id === currentFrame)
                return <span key={currentFrame} className={`${active ? 'active' : ''} ${frameId === currentFrame ? 'current' : ''}`} />
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
