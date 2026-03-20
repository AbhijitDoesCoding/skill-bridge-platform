import { useMemo, useState, useRef } from "react";
import { Github, ExternalLink } from "lucide-react";
import UploadSection from "./components/UploadSection.jsx";
import SkillGapChart from "./components/SkillGapChart.jsx";
import PathwayVisualizer from "./components/PathwayVisualizer.jsx";
import ReasoningTrace from "./components/ReasoningTrace.jsx";
import heroImg from "./hero_mockup.png";

const GITHUB_URL = "https://github.com/AbhijitDoesCoding/skill-bridge-AI-";

const API_BASE = "http://localhost:8000";

export default function App() {
  const [resumeData, setResumeData] = useState(null);
  const [jdData, setJdData] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const uploadRef = useRef(null);

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
        throw new Error(`Generation failed: ${payload?.detail || "Unknown error"}`);
      }
      setResult(payload);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const scrollToUpload = () => {
    uploadRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="page-wrapper">
      <nav className="navbar">
        <div className="logo">SkillBridge AI</div>
        <div className="nav-links">
          <a href="#about">About</a>
        </div>
      </nav>

      <header className="hero">
        <div className="hero-left">
          <h1>Bridging Potential with Opportunity</h1>
          <p>
            An AI-adaptive onboarding engine that analyzes skill gaps between your profile 
            and a target role, then generates a personalized learning pathway.
          </p>
          <button className="cta-btn" onClick={scrollToUpload}>
            Build Your Adaptive Pathway
          </button>
        </div>
        <div className="hero-right">
          <img src={heroImg} alt="Hero Mockup" />
        </div>
      </header>

      <main className="main-content" ref={uploadRef}>
        <section className="section-panel">
          <h2 className="section-title">Step 1: Document Upload</h2>
          <UploadSection 
            apiBase={API_BASE} 
            onResumeUpload={setResumeData} 
            onJobUpload={setJdData} 
          />
          
          <div style={{ marginTop: '30px', textAlign: 'center' }}>
            <button 
              className="generate-btn" 
              onClick={generatePathway} 
              disabled={!canGenerate || loading}
            >
              {loading ? "Analyzing Requirements..." : "Generate Personalized Pathway"}
            </button>
            {!canGenerate && <p className="hint-text">Upload both documents to enable analysis.</p>}
            {error && <p className="error-text">{error}</p>}
          </div>
        </section>

        {result && (
          <>
            <section className="section-panel">
              <h2 className="section-title">Step 2: Gap Analysis</h2>
              <div className="viz-wrap">
                <SkillGapChart data={result.gap_analysis} />
              </div>
            </section>

            <section className="section-panel">
              <h2 className="section-title">Step 3: Adaptive Pathway</h2>
              <div className="viz-wrap">
                <PathwayVisualizer pathway={result.pathway} />
              </div>
            </section>

            <section className="section-panel">
              <h2 className="section-title">Step 4: Reasoning Trace</h2>
              <div className="viz-wrap">
                <ReasoningTrace trace={result.reasoning_trace} />
              </div>
            </section>
          </>
        )}
      </main>

      <section className="section-panel about-section" id="about">
        <h2 className="section-title">About This Project</h2>
        <div className="about-grid">
          <div className="about-card">
            <h3>What is SkillBridge AI?</h3>
            <p>
              An AI-driven onboarding system that analyzes skill gaps between a candidate 
              profile and a target role, then generates a personalized learning pathway.
            </p>
            <ul className="feature-list">
              <li>Resume & job description parsing (PDF/text)</li>
              <li>LLM extraction via Groq API with deterministic fallback</li>
              <li>Skill normalization against a grounded taxonomy</li>
              <li>Gap analysis with readiness score</li>
              <li>DAG-based adaptive learning pathway generation</li>
              <li>Reasoning trace for transparent recommendations</li>
            </ul>
          </div>
          <div className="about-card">
            <h3>Tech Stack</h3>
            <div className="tech-badges">
              <span className="tech-badge">Python</span>
              <span className="tech-badge">FastAPI</span>
              <span className="tech-badge">React</span>
              <span className="tech-badge">Vite</span>
              <span className="tech-badge">Groq LLM</span>
              <span className="tech-badge">Recharts</span>
              <span className="tech-badge">React Flow</span>
              <span className="tech-badge">Zustand</span>
            </div>
            <h3 style={{ marginTop: '20px' }}>Quick Start</h3>
            <pre className="code-block">{`# Backend
pip install -r backend/requirements.txt
uvicorn backend.api.main:app --reload

# Frontend
cd frontend && npm install && npm run dev`}</pre>
            <a href={GITHUB_URL} target="_blank" rel="noopener noreferrer" className="github-link">
              <Github size={18} /> View on GitHub <ExternalLink size={14} />
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
