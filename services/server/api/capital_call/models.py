from datetime import datetime

from api import db


# Table for Many-to-Many Relationship
FundInvestments = db.Table(
    'fundinvestments',
    db.Column('fund_id', db.Integer,
              db.ForeignKey('fund.id')),
    db.Column('committment_id', db.Integer,
              db.ForeignKey('committment.id')),
    db.Column('capitalcall_id', db.Integer,
              db.ForeignKey('capitalcall.id')),
    db.Column('fundinvestment_id', db.Integer,
              db.ForeignKey('fundinvestment.id'))
)


class Fund(db.Model):
    __tablename__ = 'fund'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # Establish One-to-Many relationship
    committments = db.relationship(
        'Committment',
        backref='fund',
        lazy='dynamic'
    )

    # Establish Many-to-Many relationship
    investments = db.relationship(
        'Investment',
        secondary=FundInvestments,
        backref=db.backref('fund', lazy='dynamic')
    )

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.strftime('%Y-%m-%d T%H:%M:%S.%f'),
            'committments': [c.to_json() for c in self.committments],
        }


class Committment(db.Model):
    __tablename__ = 'committment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Create a foregin key for One-to-Many relationship
    fund_id = db.Column(
        db.Integer,
        db.ForeignKey('fund.id'),
        nullable=False
    )

    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # Establish Many-to-Many relationship
    investments = db.relationship(
        'Investment',
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
            'date': self.date.strftime('%Y-%m-%d T%H:%M:%S.%f'),
            'investments': [i.to_json() for i in self.investments]
        }


class CapitalCall(db.Model):
    __tablename__ = 'capitalcall'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    capital = db.Column(db.Float, nullable=False)

    # Establish Many-to-Many relationship
    investments = db.relationship(
        'Investment',
        secondary=FundInvestments,
        backref=db.backref('capitalcall', lazy='dynamic')
    )

    def __init__(self, name, capital, date=None):
        self.name = name
        self.capital = capital
        if date is not None:
            self.date = date

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'capital': self.capital,
            'date': self.date.strftime('%Y-%m-%d T%H:%M:%S.%f'),
            'investments': [i.to_json() for i in self.investments]
        }


class Investment(db.Model):
    __tablename__ = 'fundinvestment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    investment = db.Column(db.Float, nullable=False)

    def __init__(self, investment):
        self.investment = investment

    def to_json(self):
        return {
            'id': self.id,
            'investment': self.investment
        }
