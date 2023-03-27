from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src import db
from src.users.models import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session


user_schema = UserSchema()
