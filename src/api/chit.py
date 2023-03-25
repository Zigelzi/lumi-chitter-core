from flask import request
from flask_restx import Namespace, Resource, fields
from src.chits.services import create_chit

api = Namespace("chit", description="Chit related operations")

chit_fields = api.model("Chit", {"content": fields.String})


class Chit(Resource):
    def get(self):
        """Get list of chits"""
        return {"status": "OK", "message": "Chits ok"}

    @api.doc(body=chit_fields)
    def post(self):
        return create_chit(request.get_json())

    def delete(self, chit_id):
        """Delete chit by id"""
        pass


api.add_resource(Chit, "")
