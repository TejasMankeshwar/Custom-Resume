export const API_BASE_URL = "http://localhost:8000/api";

export async function checkHealth() {
  const res = await fetch(`${API_BASE_URL}/health`);
  if (!res.ok) {
    throw new Error("Failed to check backend health");
  }
  return res.json();
}

export async function createSession() {
  const res = await fetch(`${API_BASE_URL}/session`, { method: 'POST' });
  if (!res.ok) throw new Error("Failed to create session");
  return res.json();
}

export async function validateGeminiKey(apiKey: string) {
  const res = await fetch(`${API_BASE_URL}/session/validate-key`, {
    method: 'POST',
    headers: { 'x-gemini-key': apiKey }
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail?.message || "Invalid API Key");
  }
  return res.json();
}

export async function analyzeJob(sessionId: string, apiKey: string, jobDescription: string, jobTitle: string) {
  const res = await fetch(`${API_BASE_URL}/jobs/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-gemini-key': apiKey
    },
    body: JSON.stringify({ session_id: sessionId, job_description: jobDescription, job_title: jobTitle })
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail?.message || "Failed to analyze job description");
  }
  return res.json();
}

export async function generateChanges(sessionId: string, apiKey: string) {
  const res = await fetch(`${API_BASE_URL}/resume/generate-changes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-gemini-key': apiKey
    },
    body: JSON.stringify({ session_id: sessionId })
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail?.message || "Failed to generate changes");
  }
  return res.json();
}
