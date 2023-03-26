import jwt
from flask import current_app
from datetime import datetime, timedelta

from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    handle = db.Column(db.String(12), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
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
            return jwt.encode(
                token, current_app.config.get("SECRET_KEY"), algorithm="HS256"
            )
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
