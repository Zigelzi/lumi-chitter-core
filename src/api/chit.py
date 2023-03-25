from flask import request
from flask_restx import Namespace, Resource, fields
from src.chits.services import create_chit, get_all_chits, delete_chit

api = Namespace("chit", description="Chit related operations")

chit_fields = api.model("Chit", {"content": fields.String})


class ChitList(Resource):
    def get(self):
        """Get list of chits"""
        return get_all_chits()

    @api.doc(body=chit_fields)
    def post(self):
        return create_chit(request.get_json())


class Chit(Resource):
    def delete(self, chit_id):
        """Delete chit by id"""
        return delete_chit(chit_id)


api.add_resource(ChitList, "")
api.add_resource(Chit, "/<int:chit_id>")
