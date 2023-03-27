from src import db
from src.users.models import User
from src.users.schemas import user_schema


def sign_up_user(data):
    """Given serialized data, create sign up new user if handle doesn't exist"""
    existing_user = db.session.execute(
        db.select(User).filter_by(handle=data["handle"])
    ).scalar()
    if not existing_user:
        user = user_schema.load(data)
        user.save()
        db.session.commit()
        return user_schema.dump(user), 201
