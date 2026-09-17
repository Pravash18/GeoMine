"""GeoMine Flask application package."""
from flask import Flask

from .config import Config
from .db import init_app
from .errors import register_error_handlers
from .routes import api


def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or Config)
    init_app(app)
    app.register_blueprint(api, url_prefix="/api/v1")
    register_error_handlers(app)
    return app
