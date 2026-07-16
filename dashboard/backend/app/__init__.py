"""
app — Flask application factory for the Brent Oil Change Point Dashboard API.

Serves precomputed Bayesian change-point analysis results (see
../../../notebooks and ../data/build_data_artifacts.py) through a small,
versioned REST API consumed by the React frontend in ../../frontend.
"""

from flask import Flask, jsonify
from flask_cors import CORS

from app.config import get_config
from app.errors import register_error_handlers


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    from app.api import prices, changepoints, events, metrics
    app.register_blueprint(prices.bp)
    app.register_blueprint(changepoints.bp)
    app.register_blueprint(events.bp)
    app.register_blueprint(metrics.bp)

    register_error_handlers(app)

    @app.get("/api/v1/health")
    def health():
        return jsonify({"status": "ok", "service": "brent-oil-dashboard-api"})

    return app
