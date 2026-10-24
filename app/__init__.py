"""Application factory for the portfolio."""
from flask import Flask

from config import Config


def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    from app.routes import portfolio
    app.register_blueprint(portfolio)

    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        if not app.debug:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; style-src 'self'; script-src 'self'; "
                "img-src 'self' data:; object-src 'none'; base-uri 'self'; "
                "frame-ancestors 'none'; form-action 'self'"
            )
        return response

    return app
