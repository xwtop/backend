from flask import Flask

from app.blueprints import register_blueprints
from app.config.config import Config
from app.extensions import init_extensions


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)
    register_blueprints(app)

    return app
