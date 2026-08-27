import { frameImageUrl } from '../api/client.js'

export default function CameraFrame({ frame, detections }) {
  if (!frame) return <div className="empty-panel">Loading replay frames...</div>
  return (
    <div className="camera-frame">
      <img src={frameImageUrl(frame)} alt={`Driving frame ${frame.id}`} />
      <svg viewBox={`0 0 ${frame.width} ${frame.height}`} className="overlay" aria-label="Bounding box overlay">
        {frame.ground_truth.map((gt) => (
          <g key={gt.id}>
            <rect className="box gt" x={gt.bbox.x1} y={gt.bbox.y1} width={gt.bbox.x2 - gt.bbox.x1} height={gt.bbox.y2 - gt.bbox.y1} />
            <text x={gt.bbox.x1} y={gt.bbox.y1 - 8}>{gt.class_name} GT</text>
          </g>
        ))}
        {detections.map((det) => (
          <g key={det.id}>
            <rect className="box pred" x={det.bbox.x1} y={det.bbox.y1} width={det.bbox.x2 - det.bbox.x1} height={det.bbox.y2 - det.bbox.y1} />
            <text x={det.bbox.x1} y={det.bbox.y2 + 18}>T{det.track_id} {det.confidence.toFixed(2)}</text>
          </g>
        ))}
      </svg>
    </div>
  )
}
