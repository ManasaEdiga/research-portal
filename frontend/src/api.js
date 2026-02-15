const API = "http://localhost:8000";

export async function uploadFile(file) {
  const fd = new FormData();
  fd.append("file", file);
  await fetch(`${API}/upload`, { method: "POST", body: fd });
}

export async function getDocuments() {
  const res = await fetch(`${API}/documents`);
  return res.json();
}

export async function runSummary(id) {
  await fetch(`${API}/ai-summary/${id}`, { method: "POST" });
}

export async function getSummary(id) {
  const res = await fetch(`${API}/summary/${id}`);
  return res.json();
}
