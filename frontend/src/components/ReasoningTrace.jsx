export default function ReasoningTrace({ trace }) {
  return (
    <div className="trace-flex">
      <article className="trace-item">
        <h4>Extraction Reasoning</h4>
        <ul className="trace-list">
          {(trace?.extraction_reasoning || []).map((line, i) => (
            <li key={i}>{line}</li>
          ))}
        </ul>
      </article>
      <article className="trace-item">
        <h4>Gap Analysis Reasoning</h4>
        <ul className="trace-list">
          {(trace?.gap_analysis_reasoning || []).map((line, i) => (
            <li key={i}>{line}</li>
          ))}
        </ul>
      </article>
      <article className="trace-item">
        <h4>Pathway Tuning</h4>
        <ul className="trace-list">
          {(trace?.pathway_reasoning || []).map((line, i) => (
            <li key={i}>{line}</li>
          ))}
        </ul>
      </article>
    </div>
  );
}
