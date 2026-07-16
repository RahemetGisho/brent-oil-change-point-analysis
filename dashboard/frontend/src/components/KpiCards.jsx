import { formatUSD, formatPct, formatDate } from "../utils/format";

function Card({ label, value, meta, metaTone }) {
  return (
    <div className="kpi-card">
      <div className="kpi-card__label">{label}</div>
      <div className="kpi-card__value">{value}</div>
      {meta && (
        <div className={`kpi-card__meta ${metaTone ? `kpi-card__meta--${metaTone}` : ""}`}>
          {meta}
        </div>
      )}
    </div>
  );
}

export default function KpiCards({ metrics, loading }) {
  if (loading || !metrics) {
    return (
      <div className="kpi-grid">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="kpi-card">
            <div className="skeleton" style={{ height: 12, width: "60%", marginBottom: 8 }} />
            <div className="skeleton" style={{ height: 22, width: "80%" }} />
          </div>
        ))}
      </div>
    );
  }

  const { price, volatility, change_points: cp, counts } = metrics;

  return (
    <div className="kpi-grid">
      <Card
        label="Latest Price"
        value={formatUSD(price.latest)}
        meta={`Range ${formatUSD(price.min, { decimals: 0 })} – ${formatUSD(price.max, { decimals: 0 })}`}
      />
      <Card
        label="Historical Mean"
        value={formatUSD(price.mean)}
        meta={`${formatDate(price.start_date, { style: "short" })} – ${formatDate(price.end_date, { style: "short" })}`}
      />
      <Card
        label="Overall Volatility"
        value={`${volatility.overall_daily_std_pct}%`}
        meta="Daily std. dev. of log returns"
      />
      <Card
        label="Turbulent Regime Share"
        value={`${(volatility.turbulent_regime_share * 100).toFixed(1)}%`}
        meta={`${volatility.calm_regime_pct}% calm vs ${volatility.turbulent_regime_pct}% turbulent σ`}
      />
      <Card
        label="Mean-Shift Change Point"
        value={formatDate(cp.mean_shift_date, { style: "short" })}
        meta={formatPct(cp.mean_shift_pct_change)}
        metaTone={cp.mean_shift_pct_change >= 0 ? "positive" : "negative"}
      />
    </div>
  );
}
