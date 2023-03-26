from flask import Flask
from src.config import DevConfig
from src.extensions import db, ma, cors, migrate


def create_app(script_info=None):
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    register_extensions(app)

    from src.api import api_bp

    app.register_blueprint(api_bp)

    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
