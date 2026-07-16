"""
app.api.changepoints — Bayesian change point model results.

Endpoints
---------
GET /api/v1/change-points
    Returns the mean-shift (price level) and volatility-shift (log returns)
    PyMC change-point model results, each with the detected switch date,
    before/after parameter estimates, percentage change, posterior
    probability of an increase, convergence diagnostic (max r_hat), and the
    nearest matching event from the compiled calendar.

GET /api/v1/regimes
    Returns the Markov-switching model's independently-detected turbulent
    (high-volatility) regime windows, each matched to the nearest compiled
    event — used to cross-validate the change-point findings.
"""

from flask import Blueprint, jsonify

from app.data.loader import get_change_points, get_markov_regimes

bp = Blueprint("changepoints", __name__, url_prefix="/api/v1")


@bp.get("/change-points")
def change_points():
    return jsonify(get_change_points())


@bp.get("/regimes")
def regimes():
    return jsonify(get_markov_regimes())
