from flask import Blueprint
from flask_restx import Api

from src.api.chit import api as chit_ns

api_bp = Blueprint("api", __name__)

api = Api(
    api_bp, title="Chitter REST API", description="Rest API for Chitter SvelteKit app"
)

api.add_namespace(chit_ns)
