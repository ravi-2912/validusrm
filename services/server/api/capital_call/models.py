from sqlalchemy.sql import func

from api import db


class Fund(db.Model):

    __tablename__ = 'funds'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fundname = db.Column(db.String(128), nullable=False, unique=True)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, fundname):
        self.fundname = fundname

    def to_json(self):
        return {
            'id': self.id,
            'fundname': self.fundname,
        }
