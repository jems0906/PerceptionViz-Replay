export default function MetricsPanel({ metrics, frameId }) {
  const frameMetrics = metrics?.frames.find((item) => item.frame_id === frameId)
  return (
    <section className="side-panel">
      <div className="panel-title"><span>Frame metrics</span><strong>F{frameId ?? '-'}</strong></div>
      <div className="metric-stack">
        <Metric label="Precision" value={frameMetrics?.precision} />
        <Metric label="Recall" value={frameMetrics?.recall} />
        <Metric label="Mean IoU" value={frameMetrics?.mean_iou} />
        <Metric label="False positives" value={frameMetrics?.false_positives} raw />
        <Metric label="False negatives" value={frameMetrics?.false_negatives} raw />
      </div>
    </section>
  )
}

function Metric({ label, value, raw = false }) {
  const display = value === undefined ? '-' : raw ? value : `${Math.round(value * 100)}%`
  return <div className="metric-row"><span>{label}</span><strong>{display}</strong></div>
}
