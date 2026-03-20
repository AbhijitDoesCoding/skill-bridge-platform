export default function ReasoningTrace({ trace }) {
  return (
    <section className="panel">
      <h2>Reasoning Trace</h2>
      <div className="trace-grid">
        <article>
          <h3>Extraction</h3>
          <ul>
            {(trace?.extraction_reasoning || []).map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </article>
        <article>
          <h3>Gap Analysis</h3>
          <ul>
            {(trace?.gap_analysis_reasoning || []).map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </article>
        <article>
          <h3>Pathway</h3>
          <ul>
            {(trace?.pathway_reasoning || []).map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </article>
      </div>
    </section>
  );
}
