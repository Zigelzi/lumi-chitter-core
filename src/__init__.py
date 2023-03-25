from flask import Flask
from src.config import DevConfig


def create_app(script_info=None):
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    from src.api import api_bp

    app.register_blueprint(api_bp)

    return app
