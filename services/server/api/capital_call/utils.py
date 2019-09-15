from api.capital_call.funds import Fund
from api import db


PING_SUCCESS = 'Ping Successfull!'
NO_FUNDSLIST = 'No funds in database.'
YES_FUNDSLIST = 'Funds retrieved successfully.',
INVALID_PAYLD = 'Invalid payload.'
INTEGRITY_ERR = 'Integrity Error!!'
VALUE_ERR = 'Value Error!!'


def ADDED(type, x):
    return f'{type} {x} was added.'


def EXISTS(type, x):
    return f'Sorry! {type} {x} already exists.'


def NOT_EXISTS(type, x):
    return f'Sorry! {type} {x} does not exists.'


def DELETED(type, x):
    return f'{type} {x} was deleted.'


def UPDATED(type, x):
    return f'{type} {x} was updated.'


def api_response(msg, code, data=None):
    first_char = int(str(code)[0])
    return {
        'status': 'success' if first_char == 2 else 'fail',
        'message': msg,
        'data': data if data is not None else []
    }, code


def add_fund(fundname):
    fund = Fund(fundname)
    db.session.add(fund)
    db.session.commit()
    return fund


def delete(obj):
    db.session.delete(obj)
    db.session.commit()


def update(obj, key, val):
    setattr(obj, key, val)
    db.session.commit()
    return obj
