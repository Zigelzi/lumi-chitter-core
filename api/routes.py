from flask import make_response, jsonify, request

from api import app, db
from api.models import ChitSchema, Chit

# ---------------------------------
# Marshmallow serialization schemas
# ---------------------------------
chit_schema = ChitSchema()

# Status message descriptions
status_msg_fail = "fail"
status_msg_success = "success"


@app.post("/chit/")
def add_chit():
    response = {"status": status_msg_success, "data": {}}

    try:
        request_data = request.get_json()
        chit = chit_schema.load(request_data)
        chit.save()
        db.session.commit()
        response["data"]["chit"] = chit_schema.dump(chit)
        print(response)
        response["message"] = "Chit added successfully!"

        response_json = jsonify(response)

        return make_response(response_json, 200)
    except Exception as e:
        response["status"] = status_msg_fail
        response["message"] = "Something went wrong when trying to add chit"
        db.session.rollback()

        response_json = jsonify(response)
        return make_response(response_json, 500)
