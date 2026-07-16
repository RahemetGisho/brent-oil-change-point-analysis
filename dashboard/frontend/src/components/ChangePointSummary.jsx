import { formatUSD, formatPct, formatDate } from "../utils/format";

export default function ChangePointSummary({ changePoints, loading }) {
  if (loading || !changePoints) {
    return (
      <div className="cp-grid">
        <div className="skeleton" style={{ height: 140 }} />
        <div className="skeleton" style={{ height: 140 }} />
      </div>
    );
  }

  const { mean_shift: mean, variance_shift: variance } = changePoints;

  return (
    <div className="cp-grid">
      <div className="cp-card">
        <div className="cp-card__title">MEAN-SHIFT MODEL · Price Level</div>
        <div className="cp-card__date">{formatDate(mean.tau_date)}</div>
        <div className="cp-card__shift">
          <b>{formatUSD(mean.mu1)}</b> → <b>{formatUSD(mean.mu2)}</b>
          <span className="cp-card__badge">{formatPct(mean.pct_change)}</span>
        </div>
        <div className="cp-card__shift" style={{ fontSize: 12 }}>
          P(increase) = {(mean.prob_increase * 100).toFixed(0)}% · r&#770; = {mean.max_rhat.toFixed(2)}
        </div>
        {mean.nearest_event && (
          <div className="cp-card__event">
            Nearest event: <b>{mean.nearest_event.name}</b> ({formatDate(mean.nearest_event.date, { style: "short" })},{" "}
            {mean.nearest_event.gap_days}d gap)
          </div>
        )}
      </div>

      <div className="cp-card">
        <div className="cp-card__title">VOLATILITY-SHIFT MODEL · Log Returns</div>
        <div className="cp-card__date">{formatDate(variance.tau_date)}</div>
        <div className="cp-card__shift">
          <b>{variance.sigma1_pct}%</b> → <b>{variance.sigma2_pct}%</b>
          <span className="cp-card__badge">{formatPct(variance.pct_change)}</span>
        </div>
        <div className="cp-card__shift" style={{ fontSize: 12 }}>
          P(increase) = {(variance.prob_increase * 100).toFixed(0)}% · r&#770; = {variance.max_rhat.toFixed(2)}
        </div>
        {variance.nearest_event && (
          <div className="cp-card__event">
            Nearest event: <b>{variance.nearest_event.name}</b> ({formatDate(variance.nearest_event.date, { style: "short" })},{" "}
            {variance.nearest_event.gap_days}d gap)
          </div>
        )}
      </div>
    </div>
  );
}
