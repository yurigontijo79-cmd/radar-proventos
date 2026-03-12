const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`${response.status} ${response.statusText} - ${text}`);
  }

  return response.json();
}

export const api = {
  summary: () => request("/dashboard/summary"),
  upcomingEvents: () => request("/events/upcoming"),
  holdings: () => request("/holdings"),
};
