"""FutureAcad — Flask application factory."""
from datetime import datetime
from flask import Flask, render_template

from config import Config
from . import db
from .utils import ensure_csrf


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    db.init_db(app)

    # Register blueprints
    from .routes import main
    from .admin import admin
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix="/admin")

    # Inject shared template values
    @app.context_processor
    def inject_globals():
        return {"year": datetime.now().year, "csrf_token": ensure_csrf()}

    # Lightweight security headers
    @app.after_request
    def security_headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        return resp

    # Friendly error pages
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code="404",
                               heading="Lost in the network.",
                               message="The page you're looking for isn't here — but the future still is."), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("error.html", code="500",
                               heading="Something glitched.",
                               message="An unexpected error occurred. Please try again in a moment."), 500

    return app
