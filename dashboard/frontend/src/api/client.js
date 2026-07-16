const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5001/api/v1";

async function request(path, params = {}) {
  const url = new URL(`${API_BASE_URL}${path}`);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, value);
    }
  });

  const res = await fetch(url.toString());
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || `Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  health: () => request("/health"),
  prices: ({ start, end, resample } = {}) => request("/prices", { start, end, resample }),
  pricesSummary: ({ start, end } = {}) => request("/prices/summary", { start, end }),
  changePoints: () => request("/change-points"),
  regimes: () => request("/regimes"),
  events: ({ category, start, end } = {}) => request("/events", { category, start, end }),
  eventCategories: () => request("/events/categories"),
  eventDetail: (id) => request(`/events/${id}`),
  metrics: () => request("/metrics"),
};

export default api;
