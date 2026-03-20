import { useState } from "react";

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
    <section className="panel upload-grid">
      <div>
        <h2>Resume Upload</h2>
        <input type="file" accept=".pdf,.txt,.md" onChange={handleResume} disabled={busy} />
        {resumeName && <p>Uploaded: {resumeName}</p>}
      </div>
      <div>
        <h2>Job Description Upload</h2>
        <input type="file" accept=".pdf,.txt,.md" onChange={handleJob} disabled={busy} />
        {jobName && <p>Uploaded: {jobName}</p>}
      </div>
      {error && <p className="error">{error}</p>}
    </section>
  );
}
