from flask import request
from sqlalchemy import exc
from flask_restful import Resource
from sqlalchemy import select, asc

from api import db
from api.capital_call import api
from api.capital_call.models import (
    CapitalCall, Committment, Investment, FundInvestments
)
import api.capital_call.utils as UTILS


TYPE = 'Investments'


def create_obj(r, invs):
    return {
        'fund_id': r[0],
        'committment_id': r[1],
        'capitalcall_id': r[2],
        'fundinvestment_id': r[3],
        'investment': [
            i.to_json()["investment"]
            for i in invs
            if i.to_json()["id"] == r[3]
        ][0]
    }


def logic(call, committment):
    remaining_val = call.capital
    cs = []
    for c in committment:
        if 0 < remaining_val <= c.amount:
            cs.append((remaining_val, c))
            remaining_val = 0
        if remaining_val > c.amount:
            cs.append((c.amount, c))
            remaining_val = remaining_val - c.amount
    return cs


class InvestmentsPing(Resource):
    __name__ = 'InvestmentsPing'

    def get(self):
        return UTILS.api_response(
            msg=UTILS.PING_SUCCESS,
            code=200,
            data=self.__name__
        )


class InvestmentsList(Resource):
    __name__ = 'InvestmentsList'

    def get(self):
        """Get all investments"""
        investments = Investment.query.all()
        stmt = select([FundInvestments])
        res = db.session.execute(stmt).fetchall()
        obj = [create_obj(r, investments) for r in res]

        return UTILS.api_response(
            msg=UTILS.SUCCESS(TYPE, "")
            if investments else
            UTILS.NO_SUCCESS(TYPE, ""),
            code=200 if investments else 404,
            data={'fundinvestments': obj}
        )

    def post(self):
        post_data = request.get_json()
        if not post_data:
            return UTILS.api_response(
                msg=UTILS.INVALID_PAYLD,
                code=400,
                data=self.__name__
            )
        call_id = post_data.get('call_id')
        rule = post_data.get('rule')
        try:
            call = CapitalCall.query.filter_by(id=int(call_id)).first()
            committments = []
            if rule == 'fifo':
                committments = Committment.query \
                    .order_by(asc(Committment.date)).all()
            committments_used = logic(call, committments)
            fundinvestments = []
            for amount, committment in committments_used:
                fi = UTILS.add_fundinvestment(amount, committment, call)
                fundinvestments.append({
                    'fund_id': committment.fund_id,
                    'committment_id': committment.id,
                    'capitalcall_id': call.id,
                    'fundinvestment_id': fi.id,
                    'investment': fi.investment
                })

            return UTILS.api_response(
                msg=UTILS.ADDED(TYPE, f'for Capital Call ID {call.id}'),
                code=201,
                data={
                    'fundinvestments': [fi for fi in fundinvestments]
                }
            )
        except exc.IntegrityError as e:
            db.session.rollback()
            return UTILS.api_response(
                msg=f'{UTILS.INTEGRITY_ERR} {self.__name__}',
                code=400,
                data=f'{str(e)}'
            )


class Investments(Resource):
    __name__ = 'Investments'

    def get(self, investment_id):
        """Get single investment details"""
        try:
            inv = Investment.query.filter_by(id=int(investment_id)).first()
            stmt = FundInvestments.select().where(
                FundInvestments.c.fundinvestment_id == int(investment_id)
            )
            res = db.session.execute(stmt).fetchall()
            obj = [create_obj(r, [inv]) for r in res][0]
            if not inv:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, investment_id),
                    code=404,
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.SUCCESS(TYPE, inv.id),
                    code=200,
                    data=obj
                )
        except ValueError as e:
            return UTILS.api_response(
                msg=f'{UTILS.VALUE_ERR} {self.__name__}',
                code=404,
                data=f'{str(e)}'
            )

    def put(self):
        pass

    def delete(self, investment_id):
        """Delete single investment details"""
        try:
            inv = Investment.query.filter_by(id=int(investment_id)).first()

            if not inv:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, investment_id),
                    code=404,
                )
            else:
                UTILS.delete(inv)
                return UTILS.api_response(
                    msg=UTILS.DELETED(TYPE, inv.id),
                    code=200
                )
        except ValueError as e:
            return UTILS.api_response(
                msg=f'{UTILS.VALUE_ERR} {self.__name__}',
                code=404,
                data=f'{str(e)}'
            )


api.add_resource(InvestmentsPing, '/investments/ping')
api.add_resource(InvestmentsList, '/investments')
api.add_resource(Investments, '/investments/<investment_id>')
