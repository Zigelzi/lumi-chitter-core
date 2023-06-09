import traceback
from flask import make_response, jsonify, request

from api import app, db
from api.models import ChitSchema, UserSchema, User, Chit

# ---------------------------------
# Marshmallow serialization schemas
# ---------------------------------
chit_schema = ChitSchema()
chits_schema = ChitSchema(many=True)
user_schema = UserSchema()

# Status message descriptions
status_msg_fail = "fail"
status_msg_success = "success"


@app.get("/chit/")
def get_all_chits():
    response = {"status": status_msg_success}
    if not request.cookies.get("token"):
        response["status"] = status_msg_fail
        response["message"] = "Not authorized!"
        return make_response(jsonify(response), 500)
    try:
        chits = Chit.get_all()
        response["chits"] = chits_schema.dump(chits)
        response["message"] = "Chits queried successfully!"
        return make_response(jsonify(response), 200)
    except Exception as e:
        response["status"] = status_msg_fail
        response["message"] = "Something went wrong when trying to query all chits"
        return make_response(jsonify(response), 500)


@app.post("/chit/")
def add_chit():
    response = {"status": status_msg_success, "data": {}}
    try:
        request_data = request.get_json()

        user = db.session.get(User, request_data["author"]["id"])
        if user:
            chit = chit_schema.load(request_data)
            chit.save()
            db.session.commit()
            response["chit"] = chit_schema.dump(chit)
            response["message"] = "Chit added successfully!"
            return make_response(jsonify(response), 200)
        else:
            response["status"] = status_msg_fail
            response["message"] = "Author was not found"
            return make_response(jsonify(response), 500)
    except Exception as e:
        traceback.print_exc()
        response["status"] = status_msg_fail
        response["message"] = "Something went wrong when trying to add chit"
        db.session.rollback()
        return make_response(jsonify(response), 500)


@app.delete("/chit/<int:chit_id>")
def delete_chit(chit_id):
    response = {"status": status_msg_success, "data": {}}
    try:
        request_data = request.get_json()
        author = db.session.get(User, request_data["chit"]["author"]["id"])
        chit = db.session.get(Chit, chit_id)
        if chit:
            db.session.delete(chit)
            db.session.commit()
            response["message"] = "Chit deleted successfully!"
            return make_response(jsonify(response), 200)
        else:
            response["status"] = status_msg_fail
            response["message"] = "Chit was not found"
            return make_response(jsonify(response), 500)
    except Exception as e:
        traceback.print_exc()
        response["status"] = status_msg_fail
        response["message"] = "Something went wrong when trying to delete chit"
        db.session.rollback()
        return make_response(jsonify(response), 500)


@app.post("/user/")
def add_user():
    response = {"status": status_msg_success, "data": {}}
    try:
        request_data = request.get_json()
        user = db.session.execute(
            db.select(User).filter_by(handle=request_data["handle"])
        ).first()
        if not user:
            user = user_schema.load(request_data)
            user.save()
            db.session.commit()
            auth_token = user.encode_auth_token(user.id)
            response["message"] = "User added successfully!"
            response["user"] = user_schema.dump(user)
            response["token"] = auth_token
            print(auth_token)
            return make_response(jsonify(response), 200)
        else:
            response["status"] = status_msg_fail
            response[
                "message"
            ] = "User with this handle already exists, select another handle."
            return make_response(jsonify(response), 422)
    except Exception as e:
        traceback.print_exc()
        response["status"] = status_msg_fail
        response["message"] = "Something went wrong when trying to add user"
        db.session.rollback()
        return make_response(jsonify(response), 500)


@app.post("/auth/login")
def login():
    response = {"status": status_msg_success, "data": {}}
    try:
        request_data = request.get_json()
        user = db.session.execute(
            db.select(User).filter_by(handle=request_data["handle"])
        ).first()
        return make_response(jsonify(response), 200)
    except Exception as e:
        traceback.print_exc()
        response["status"] = status_msg_fail
        response["message"] = "Something went wrong when trying to login user"
        return make_response(jsonify(response), 500)
