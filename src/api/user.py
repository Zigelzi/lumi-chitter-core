from flask import request
from flask_restx import Namespace, Resource, fields
from src.users.services import sign_up_user, get_all_users

api = Namespace("user", description="User related operations")

user_fields = api.model("User", {"name": fields.String, "handle": fields.String})


class UserList(Resource):
    def get(self):
        return get_all_users()

    @api.doc(body=user_fields)
    def post(self):
        return sign_up_user(request.get_json())


api.add_resource(UserList, "")
