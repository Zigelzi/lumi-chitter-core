from flask import make_response, jsonify

from api import app

# Status message descriptions
status_msg_fail = "fail"
status_msg_success = "success"

likes = []


@app.get("/likes/<string:chit_id>")
def get_likes(chit_id):
    response = {"status": status_msg_success, "chit_id": chit_id}
    print(response)
    response_json = jsonify(response)

    return make_response(response_json, 200)


@app.post("/likes/<string:chit_id>")
def add_like(chit_id):
    response = {"status": status_msg_success, "chit_id": chit_id}
    likes.append({"chit_id": chit_id})
    response["likes"] = likes

    response_json = jsonify(response)
    print(likes)

    return make_response(response_json, 200)
