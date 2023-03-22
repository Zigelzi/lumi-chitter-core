from api import db, ma

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Chit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    @staticmethod
    def get_all():
        return Chit.query.all()

    def __repr__(self):
        return f"<Chit {self.id} | {self.content}>"


# ---------------------------------
# Marshmallow serialization schemas
# ---------------------------------
class ChitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Chit
        load_instance = True
        sqla_session = db.session
