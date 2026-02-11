from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        response = {
            "error": exc.name,
            "message": exc.description,
        }
        return jsonify(response), exc.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(exc: Exception):
        app.logger.exception("Unhandled exception: %s", exc)
        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred.",
        }
        return jsonify(response), 500
