const API_BASE = import.meta.env.VITE_API_BASE || `http://${window.location.hostname}:5000`;

export async function getAccounts() {
  const res = await fetch(`${API_BASE}/api/accounts`);
  return res.json();
}

export async function getDealerships(accountId) {
  const res = await fetch(`${API_BASE}/api/accounts/${accountId}/dealerships`);
  return res.json();
}

export async function uploadBackground(file) {
  const formData = new FormData();
  formData.append('background', file);
  const res = await fetch(`${API_BASE}/api/upload/background`, { method: 'POST', body: formData });
  return res.json();
}

export async function generateCreatives(payload) {
  const res = await fetch(`${API_BASE}/api/generate-creatives`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export function fullUrl(path) {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  return `${API_BASE}${path}`;
}

export async function login(email, password) {
  const res = await fetch(`${API_BASE}/api/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  return res.json();
}
