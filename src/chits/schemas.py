from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src import db
from src.chits.models import Chit


class ChitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Chit
        load_instance = True
        sqla_session = db.session
        ordered = True


chit_schema = ChitSchema()
chit_list_schema = ChitSchema(many=True)
