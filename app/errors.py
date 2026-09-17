"""Consistent JSON error responses."""
from flask import jsonify


def _error(code, message, status):
    return jsonify({"error": {"code": code, "message": message}}), status


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_error):
        return _error_response("NOT_FOUND", "Resource not found.", 404)

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return _error_response("METHOD_NOT_ALLOWED", "HTTP method not allowed.", 405)

    @app.errorhandler(500)
    def internal_error(_error):
        return _error_response("INTERNAL_ERROR", "An unexpected server error occurred.", 500)


def _error_response(code, message, status):
    return jsonify({"error": {"code": code, "message": message}}), status
