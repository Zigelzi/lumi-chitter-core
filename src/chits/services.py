from src import db
from src.chits.models import Chit
from src.chits.schemas import chit_list_schema, chit_schema


def get_all_chits():
    chits = Chit.get_all()
    return chit_list_schema.dump(chits), 200


def create_chit(data):
    """Given serialized data, deserialize it and create a new chit"""
    chit = chit_schema.load(data)
    chit.save()
    db.session.commit()
    return chit_schema.dump(chit), 201


def delete_chit(chit_id):
    response = {"message": ""}
    chit = db.session.execute(db.select(Chit).where(Chit.id == chit_id)).scalar()
    if not chit:
        response["message"] = f"Chit with ID {chit_id} does not exist"
        return response, 404

    db.session.delete(chit)
    db.session.commit()
    response["message"] = f"Chit {chit_id} deleted successfully"
    return response, 200
