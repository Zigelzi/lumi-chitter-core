from datetime import datetime, timezone
from src import db

Column = db.Column
Model = db.Model


class Chit(Model):
    id = Column(db.Integer, primary_key=True)
    content = Column(db.String, nullable=False)
    # user_id = Column(db.Integer, db.ForeignKey("user.id"))
    created_at = Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    @staticmethod
    def get_all():
        return Chit.query.all()

    def __repr__(self):
        return f"<Chit {self.id} | {self.content[0:10]}>"
