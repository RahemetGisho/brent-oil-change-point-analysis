export function formatUSD(value, { decimals = 2 } = {}) {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return `$${Number(value).toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })}`;
}

export function formatPct(value, { decimals = 1, signed = true } = {}) {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  const sign = signed && value > 0 ? "+" : "";
  return `${sign}${Number(value).toFixed(decimals)}%`;
}

export function formatDate(dateStr, { style = "medium" } = {}) {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  if (Number.isNaN(d.getTime())) return dateStr;
  const options =
    style === "short"
      ? { year: "numeric", month: "short" }
      : { year: "numeric", month: "short", day: "numeric" };
  return d.toLocaleDateString("en-US", options);
}

export const CATEGORY_COLORS = {
  Conflict: "#C0392B",
  "Conflict / Sanctions": "#8E3B46",
  Sanctions: "#8E44AD",
  "OPEC Policy": "#D68910",
  "OPEC Policy / Supply Glut": "#B9770E",
  "Economic Shock": "#2471A3",
  Geopolitical: "#17A398",
  "Market Peak": "#5D6D7E",
};

export function categoryColor(category) {
  return CATEGORY_COLORS[category] || "#5D6D7E";
}
