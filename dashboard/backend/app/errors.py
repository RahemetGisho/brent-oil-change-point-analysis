"""app.errors — consistent JSON error responses for the API."""

from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not found", "detail": str(e)}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "bad request", "detail": str(e)}), 400

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "internal server error"}), 500
