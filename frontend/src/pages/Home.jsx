export default function Home({ metrics, status }) {
  return (
    <main className="overview-grid">
      <section className="hero-panel">
        <p className="eyebrow">Autonomy model + visualization</p>
        <h2>Replay sampled driving frames, inspect detections, and trace tracker behavior.</h2>
        <p>
          The app ships with synthetic camera frames and ground truth, precomputes YOLO-style outputs for fast Railway loads,
          stores detections in Parquet, and exports replay messages to MCAP for Foxglove-style workflows.
        </p>
      </section>
      <section className="metric-strip">
        <div>
          <span>Backend</span>
          <strong>{status}</strong>
        </div>
        <div>
          <span>Precision</span>
          <strong>{metrics ? `${Math.round(metrics.precision * 100)}%` : '-'}</strong>
        </div>
        <div>
          <span>Recall</span>
          <strong>{metrics ? `${Math.round(metrics.recall * 100)}%` : '-'}</strong>
        </div>
        <div>
          <span>ID switches</span>
          <strong>{metrics?.id_switches ?? '-'}</strong>
        </div>
      </section>
    </main>
  )
}
