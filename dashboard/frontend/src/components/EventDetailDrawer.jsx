import { formatUSD, formatPct, formatDate, categoryColor } from "../utils/format";

export default function EventDetailDrawer({ event, onClose }) {
  if (!event) return null;
  const impact = event.impact || {};

  return (
    <div className="drawer-backdrop" onClick={onClose}>
      <div className="drawer" onClick={(e) => e.stopPropagation()}>
        <button className="drawer__close" onClick={onClose} aria-label="Close">
          ✕
        </button>
        <span
          className="drawer__category"
          style={{ background: categoryColor(event.category) }}
        >
          {event.category}
        </span>
        <div className="drawer__title">{event.name}</div>
        <div className="drawer__date">
          {formatDate(event.start_date)}
          {event.end_date && event.end_date !== event.start_date
            ? ` – ${formatDate(event.end_date)}`
            : ""}
        </div>

        <p className="drawer__description">{event.description}</p>

        <div className="drawer__stats">
          <div className="drawer__stat">
            <div className="drawer__stat-label">Price before (90d avg)</div>
            <div className="drawer__stat-value">{formatUSD(impact.price_before)}</div>
          </div>
          <div className="drawer__stat">
            <div className="drawer__stat-label">Price after (90d avg)</div>
            <div className="drawer__stat-value">{formatUSD(impact.price_after)}</div>
          </div>
          <div className="drawer__stat">
            <div className="drawer__stat-label">Price change</div>
            <div className="drawer__stat-value">{formatPct(impact.pct_change)}</div>
          </div>
          <div className="drawer__stat">
            <div className="drawer__stat-label">Expected direction</div>
            <div className="drawer__stat-value">{event.expected_direction}</div>
          </div>
          <div className="drawer__stat">
            <div className="drawer__stat-label">Volatility before</div>
            <div className="drawer__stat-value">{impact.volatility_before_pct}%</div>
          </div>
          <div className="drawer__stat">
            <div className="drawer__stat-label">Volatility after</div>
            <div className="drawer__stat-value">{impact.volatility_after_pct}%</div>
          </div>
        </div>

        <span className={`confirm-badge ${impact.direction_confirmed ? "confirm-badge--yes" : "confirm-badge--no"}`}>
          {impact.direction_confirmed ? "✓ Matches expected direction" : "◐ Did not match expected direction"}
        </span>

        <p style={{ fontSize: 11.5, color: "#94a3b8", marginTop: 20, lineHeight: 1.6 }}>
          Price/volatility figures are empirical averages in a ±90-day window around the
          event date — a temporal association, not proof that this event caused the change.
        </p>
      </div>
    </div>
  );
}
