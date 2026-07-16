"""
app.api.metrics — headline KPIs for the dashboard's summary cards.

GET /api/v1/metrics
    Returns a compact set of indicators combining the price series, the
    change-point results, and the Markov-switching regime analysis:
    overall price range/mean, calm vs. turbulent volatility, the turbulent
    regime's share of trading days, and counts of events/change points.
"""

import numpy as np
from flask import Blueprint, jsonify

from app.data.loader import get_prices_df, get_events, get_change_points, get_markov_regimes

bp = Blueprint("metrics", __name__, url_prefix="/api/v1/metrics")


@bp.get("")
def metrics():
    df = get_prices_df()
    events = get_events()
    change_points = get_change_points()
    regimes = get_markov_regimes()

    returns = np.log(df["Price"] / df["Price"].shift(1)).dropna()

    return jsonify({
        "price": {
            "start_date": df["Date"].min().strftime("%Y-%m-%d"),
            "end_date": df["Date"].max().strftime("%Y-%m-%d"),
            "min": round(float(df["Price"].min()), 2),
            "max": round(float(df["Price"].max()), 2),
            "mean": round(float(df["Price"].mean()), 2),
            "latest": round(float(df["Price"].iloc[-1]), 2),
        },
        "volatility": {
            "overall_daily_std_pct": round(float(returns.std()) * 100, 2),
            "calm_regime_pct": regimes["calm_sigma_pct"],
            "turbulent_regime_pct": regimes["turbulent_sigma_pct"],
            "turbulent_regime_share": regimes["high_volatility_regime_share"],
        },
        "change_points": {
            "mean_shift_date": change_points["mean_shift"]["tau_date"],
            "mean_shift_pct_change": change_points["mean_shift"]["pct_change"],
            "volatility_shift_date": change_points["variance_shift"]["tau_date"],
            "volatility_shift_pct_change": change_points["variance_shift"]["pct_change"],
        },
        "counts": {
            "events": len(events),
            "turbulent_regime_windows": len(regimes["windows"]),
            "trading_days": int(len(df)),
        },
    })
