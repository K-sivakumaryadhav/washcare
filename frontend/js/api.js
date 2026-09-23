// Same-origin API calls — backend serves this frontend, so no base URL needed.
// If you deploy frontend and backend separately, set this to the backend's URL.
const API_BASE = "";

async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
  return res.json();
}

async function apiPost(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(extractErrorMessage(err) || `POST ${path} failed: ${res.status}`);
  }
  return res.json();
}

// FastAPI validation errors (422) come back as {"detail": [{"msg": "...", ...}]}
// rather than a plain string — pull out a readable message either way.
function extractErrorMessage(err) {
  if (!err || !err.detail) return null;
  if (typeof err.detail === "string") return err.detail;
  if (Array.isArray(err.detail) && err.detail[0]) {
    return err.detail[0].msg || JSON.stringify(err.detail[0]);
  }
  return null;
}
