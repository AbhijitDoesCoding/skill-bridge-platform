import { useState } from "react";
import { UploadCloud, FileText, CheckCircle, Loader2 } from "lucide-react";

async function uploadFile(apiBase, endpoint, file) {
  const body = new FormData();
  body.append("file", file);

  const response = await fetch(`${apiBase}${endpoint}`, {
    method: "POST",
    body,
  });

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.status}`);
  }
  return response.json();
}

export default function UploadSection({ apiBase, onResumeUpload, onJobUpload }) {
  const [resumeName, setResumeName] = useState("");
  const [jobName, setJobName] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const handleResume = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setBusy(true);
    setError("");
    try {
      const payload = await uploadFile(apiBase, "/api/upload/resume", file);
      onResumeUpload(payload.data);
      setResumeName(file.name);
    } catch (err) {
      setError(err.message || "Failed to upload resume");
    } finally {
      setBusy(false);
    }
  };

  const handleJob = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setBusy(true);
    setError("");
    try {
      const payload = await uploadFile(apiBase, "/api/upload/job-description", file);
      onJobUpload(payload.data);
      setJobName(file.name);
    } catch (err) {
      setError(err.message || "Failed to upload job description");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="upload-grid">
      <label className="upload-card">
        <input type="file" accept=".pdf,.txt,.md" onChange={handleResume} disabled={busy} />
        <div className="icon">
          {busy ? <Loader2 size={40} className="animate-spin" /> : 
           resumeName ? <CheckCircle size={40} color="#4caf50" /> : <UploadCloud size={40} />}
        </div>
        <h3>Resume Document</h3>
        <p>{resumeName || "Drop your PDF or click to browse"}</p>
      </label>

      <label className="upload-card">
        <input type="file" accept=".pdf,.txt,.md" onChange={handleJob} disabled={busy} />
        <div className="icon">
          {busy ? <Loader2 size={40} className="animate-spin" /> : 
           jobName ? <CheckCircle size={40} color="#4caf50" /> : <FileText size={40} />}
        </div>
        <h3>Job Description</h3>
        <p>{jobName || "Upload target role requirements"}</p>
      </label>

      {error && <p className="error-text" style={{ gridColumn: 'span 2' }}>{error}</p>}
    </div>
  );
}
