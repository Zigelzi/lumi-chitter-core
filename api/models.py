import jwt
from datetime import datetime, timedelta
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from api import db, ma, app


class Chit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    @staticmethod
    def get_all():
        return Chit.query.all()

    def __repr__(self):
        return f"<Chit {self.id} | {self.content}>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    handle = db.Column(db.String(12), unique=True, nullable=False)
    chits = db.relationship("Chit", backref="author", lazy="dynamic")

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        lifetime = timedelta(days=0, minutes=60)
        expires_on = datetime.utcnow() + lifetime

        try:
            token = {
                "exp": expires_on,
                "iat": datetime.utcnow(),
                "sub": user_id,  # Subject
            }
            return jwt.encode(token, app.config.get("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def decode_auth_token(token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            token = jwt.decode(token, app.config.get("SECRET_KEY"))
            return token["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    def __repr__(self):
        return f"<User {self.id} | {self.name} | {self.handle}>"


# ---------------------------------
# Marshmallow serialization schemas
# ---------------------------------
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session


class ChitSchema(SQLAlchemyAutoSchema):
    author = Nested(UserSchema)

    class Meta:
        model = Chit
        load_instance = True
        sqla_session = db.session
