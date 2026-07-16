import { formatDate } from "../utils/format";

export default function RegimePanel({ regimes, loading }) {
  if (loading || !regimes) {
    return <div className="skeleton" style={{ height: 200 }} />;
  }

  return (
    <div>
      <p style={{ fontSize: 12.5, color: "#64748b", marginBottom: 14, lineHeight: 1.6 }}>
        A 2-regime Markov-switching model (fit independently of the event calendar) estimates
        the market spends <b>{(1 - regimes.high_volatility_regime_share) * 100 | 0}%</b> of days in a
        calm regime (σ ≈ {regimes.calm_sigma_pct}%/day) and{" "}
        <b>{(regimes.high_volatility_regime_share * 100).toFixed(1)}%</b> in a turbulent regime
        (σ ≈ {regimes.turbulent_sigma_pct}%/day). It detected {regimes.windows.length} turbulent
        windows below.
      </p>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12.5 }}>
          <thead>
            <tr style={{ textAlign: "left", color: "#64748b", borderBottom: "1px solid #eef2f6" }}>
              <th style={{ padding: "6px 8px" }}>Window start</th>
              <th style={{ padding: "6px 8px" }}>Window end</th>
              <th style={{ padding: "6px 8px" }}>Trading days</th>
              <th style={{ padding: "6px 8px" }}>Nearest event</th>
              <th style={{ padding: "6px 8px" }}>Gap</th>
            </tr>
          </thead>
          <tbody>
            {regimes.windows.map((w, i) => (
              <tr key={i} style={{ borderBottom: "1px solid #f3f6f9" }}>
                <td style={{ padding: "7px 8px", fontVariantNumeric: "tabular-nums" }}>
                  {formatDate(w.start_date, { style: "short" })}
                </td>
                <td style={{ padding: "7px 8px", fontVariantNumeric: "tabular-nums" }}>
                  {formatDate(w.end_date, { style: "short" })}
                </td>
                <td style={{ padding: "7px 8px" }}>{w.trading_days}</td>
                <td style={{ padding: "7px 8px", fontWeight: 600 }}>
                  {w.nearest_event?.name || "—"}
                </td>
                <td style={{ padding: "7px 8px", color: w.nearest_event?.gap_days <= 14 ? "#1e8e5a" : "#94a3b8" }}>
                  {w.nearest_event ? `${w.nearest_event.gap_days}d` : "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
