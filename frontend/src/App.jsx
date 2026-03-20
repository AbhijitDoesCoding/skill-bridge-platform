import { useMemo, useState } from "react";
import UploadSection from "./components/UploadSection.jsx";
import SkillGapChart from "./components/SkillGapChart.jsx";
import PathwayVisualizer from "./components/PathwayVisualizer.jsx";
import ReasoningTrace from "./components/ReasoningTrace.jsx";

const API_BASE = "http://localhost:8000";

export default function App() {
  const [resumeData, setResumeData] = useState(null);
  const [jdData, setJdData] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const canGenerate = useMemo(() => Boolean(resumeData && jdData), [resumeData, jdData]);

  const generatePathway = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/api/analyze/pathway`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          resume_data: resumeData,
          jd_data: jdData,
          preferences: { time_budget_hours: 120 },
        }),
      });
      const payload = await response.json();
      if (!response.ok) {
        const detail =
          typeof payload?.detail === "string"
            ? payload.detail
            : JSON.stringify(payload?.detail || payload);
        throw new Error(`Pathway generation failed (${response.status}): ${detail}`);
      }
      setResult(payload);
    } catch (err) {
      setError(err.message || "Unexpected error while generating pathway");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="hero">
        <div className="hero-content">
          <h1>AI-Adaptive Onboarding Engine</h1>
          <p>Upload a resume and job description to generate a grounded learning roadmap.</p>
        </div>
      </header>

      <main className="container">
        <UploadSection apiBase={API_BASE} onResumeUpload={setResumeData} onJobUpload={setJdData} />

        <section className="panel action-panel">
          <button onClick={generatePathway} disabled={!canGenerate || loading}>
            {loading ? "Generating Pathway..." : "Generate Learning Pathway"}
          </button>
          {!canGenerate && <p>Upload both documents to enable pathway generation.</p>}
          {error && <p className="error">{error}</p>}
        </section>

        {result && (
          <>
            <SkillGapChart data={result.gap_analysis} />
            <PathwayVisualizer pathway={result.pathway} />
            <ReasoningTrace trace={result.reasoning_trace} />
          </>
        )}
      </main>
    </div>
  );
}
