from src import db
from src.chits.models import Chit
from src.chits.schemas import chit_list_schema, chit_schema


def create_chit(data):
    """Given serialized data, deserialize it and create a new chit"""
    chit = chit_schema.load(data)
    chit.save()
    db.session.commit()
    return chit_schema.dump(chit), 201
