import datetime

from api import db


# Table for Many-to-Many Relationship
FundInvestments = db.Table(
    'fundinvestments',
    db.Column(
        'capitalcall_id',
        db.Integer,
        db.ForeignKey('capitalcall.id')
    ),
    db.Column(
        'committment_id',
        db.Integer,
        db.ForeignKey('committment.id')
    ),
    db.Column(
        'fundinvestment_id',
        db.Integer,
        db.ForeignKey('fundinvestment.id')
    )
)


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

    # Establishing Many-to-Many Relationship
    fundinvestments = db.relationship(
        'FundInvestment',
        secondary=FundInvestments,
        backref=db.backref('committment', lazy='dynamic')
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


class CapitalCall(db.Model):
    __tablename__ = 'capitalcall'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(
        db.DateTime,
        default=datetime.datetime.now(),
        nullable=False
    )
    investment_name = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )
    capital_requirement = db.Column(db.Float, nullable=False)

    # Establishing Many-to-Many Relationship
    fundinvestments = db.relationship(
        'FundInvestment',
        secondary=FundInvestments,
        backref=db.backref('capitalcall', lazy='dynamic')
    )

    def __init__(self, investment_name, capital_requirement, date=None):
        self.investment_name = investment_name
        self.capital_requirement = capital_requirement
        if date is not None:
            self.date = date

    def to_json(self):
        return {
            'id': self.id,
            'investment_name': self.investment_name,
            'capital_requirement': self.capital_requirement,
            'date': self.date
        }


class FundInvestment(db.Model):
    __tablename__ = 'fundinvestment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    investment_amount = db.Column(db.Float, nullable=False)

    def __init__(self, investment_amount):
        self.investment_amount = investment_amount

    def to_json(self):
        return {
            'id': self.id,
            'investment_amount': self.investment_amount
        }
