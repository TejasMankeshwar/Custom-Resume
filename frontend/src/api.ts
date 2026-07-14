export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8001/api";

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

export async function validateGeminiKey(apiKey: string, model: string = 'gemini-3.5-flash') {
  const res = await fetch(`${API_BASE_URL}/session/validate-key`, {
    method: 'POST',
    headers: { 'x-gemini-key': apiKey, 'x-gemini-model': model }
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail?.message || "Invalid API Key");
  }
  return res.json();
}

export async function analyzeJob(sessionId: string, apiKey: string, model: string, jobDescription: string, jobTitle: string) {
  const res = await fetch(`${API_BASE_URL}/jobs/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-gemini-key': apiKey,
      'x-gemini-model': model
    },
    body: JSON.stringify({ session_id: sessionId, job_description: jobDescription, job_title: jobTitle })
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail?.message || "Failed to analyze job description");
  }
  return res.json();
}

export async function generateChanges(sessionId: string, apiKey: string, model: string) {
  const res = await fetch(`${API_BASE_URL}/resume/generate-changes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-gemini-key': apiKey,
      'x-gemini-model': model
    },
    body: JSON.stringify({ session_id: sessionId })
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail?.message || "Failed to generate changes");
  }
  return res.json();
}

export async function generateResume(sessionId: string, decisions: Record<string, string>) {
  const res = await fetch(`${API_BASE_URL}/resume/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ session_id: sessionId, decisions })
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail?.message || "Failed to generate resume");
  }
  return res.json();
}

export async function compileResume(sessionId: string) {
  const res = await fetch(`${API_BASE_URL}/resume/compile`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ session_id: sessionId })
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail?.message || "Failed to compile resume");
  }
  return res.json();
}

