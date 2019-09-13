import datetime

from api import db


class Fund(db.Model):
    __tablename__ = 'fund'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fundname = db.Column(db.String(128), nullable=False, unique=True)
    date = db.Column(
        db.DateTime,
        default=datetime.datetime.now(),
        nullable=False
    )

    committments = db.relationship(
        'Committment',
        backref='fund',
        lazy='dynamic'
    )

    def __init__(self, fundname):
        self.fundname = fundname

    def to_json(self):
        return {
            'id': self.id,
            'fundname': self.fundname,
        }


class Committment(db.Model):
    __tablename__ = 'committment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fund_id = db.Column(
        db.Integer,
        db.ForeignKey('fund.id'),
        nullable=False
    )
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(
        db.DateTime,
        default=datetime.datetime.now(),
        nullable=False
    )

    def __init__(self, fund_id, amount, date=None):
        self.amount = amount
        self.fund_id = fund_id
        if date is not None:
            self.date = date

    def to_json(self):
        return {
            'id': self.id,
            'fund_id': self.fund_id,
            'amount': self.amount,
            'date': self.date
        }
