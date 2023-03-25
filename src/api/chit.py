from flask_restx import Namespace, Resource

api = Namespace("chit", description="Chit related operations")


class Chit(Resource):
    def get(self):
        return {"status": "OK", "message": "Chits ok"}


api.add_resource(Chit, "")
