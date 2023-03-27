from src import db
from src.users.models import User
from src.users.schemas import user_schema, user_list_schema


def get_all_users():
    users = User.get_all()
    return user_list_schema.dump(users), 200


def sign_up_user(data):
    """Given serialized data, create sign up new user if handle doesn't exist"""
    response = {"message": ""}

    existing_user = db.session.execute(
        db.select(User).filter_by(handle=data["handle"])
    ).scalar()
    if existing_user:
        response[
            "message"
        ] = f"User with handle {existing_user.handle} already exists. Select new handle"
        return response, 400
    user = user_schema.load(data)
    user.save()
    db.session.commit()
    return user_schema.dump(user), 201
