from flask import request
from sqlalchemy import exc
from flask_restful import Resource

from api import db
from api.capital_call import api
from api.capital_call.models import CapitalCall
import api.capital_call.utils as UTILS


TYPE = 'CapitalCall'


class CapitalcallsPing(Resource):
    __name__ = 'CapitalcallsPing'

    def get(self):
        return UTILS.api_response(
            msg=UTILS.PING_SUCCESS,
            code=200,
            data=self.__name__
        )


class CapitalcallsList(Resource):
    __name__ = 'CapitalcallsList'

    def get(self):
        """Get all capitalcalls"""
        capitalcalls = CapitalCall.query.all()
        return UTILS.api_response(
            msg=(UTILS.YES_FUNDSLIST
                 if capitalcalls
                 else UTILS.NO_FUNDSLIST),
            code=200,
            data={'capitalcalls': [c.to_json() for c in capitalcalls]}
        )

    def post(self):
        post_data = request.get_json()
        if not post_data:
            return UTILS.api_response(
                msg=UTILS.INVALID_PAYLD,
                code=400,
                data=self.__name__
            )
        fund_id = post_data.get('fund_id')
        amount = post_data.get('amount')
        try:
            capitalcall = UTILS.add_capitalcall(fund_id, amount)
            return UTILS.api_response(
                msg=UTILS.ADDED(TYPE, f'{capitalcall.id} in fund {fund_id}'),
                code=201,
                data=capitalcall.to_json()
                )
        except exc.IntegrityError as e:
            db.session.rollback()
            return UTILS.api_response(
                msg=f'{UTILS.INTEGRITY_ERR} {self.__name__}',
                code=400,
                data=f'{str(e)}'
            )


class Capitalcalls(Resource):
    __name__ = 'Capitalcalls'

    def get(self, capitalcall_id):
        """Get single capitalcall details"""
        try:
            capitalcall = Capitalcall.query \
                            .filter_by(id=int(capitalcall_id)) \
                            .first()
            if not capitalcall:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, capitalcall_id),
                    code=404,
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.SUCCESS(TYPE, capitalcall.id),
                    code=200,
                    data=capitalcall.to_json()
                )
        except ValueError as e:
            return UTILS.api_response(
                msg=f'{UTILS.VALUE_ERR} {self.__name__}',
                code=404,
                data=f'{str(e)}'
            )

    def put(self, capitalcall_id):
        """Update single capitalcall details"""
        put_data = request.get_json()
        fund_id = put_data.get('fund_id')
        amount = put_data.get("amount")
        date = put_data.get("date")
        if not put_data:
            return UTILS.api_response(
                msg=UTILS.INVALID_PAYLD,
                code=405
            )
        try:
            c = Capitalcall.query.get(capitalcall_id)
            if c:
                if fund_id:
                    if fund_id != c.fund_id:
                        c = UTILS.update(c, 'fund_id', int(fund_id))
                    else:
                        return UTILS.api_response(
                            msg=UTILS.NO_CHANGE(
                                TYPE, f'{c.id} in fund {c.fund_id}'
                            ),
                            code=400,
                            data=c.query.get(capitalcall_id).to_json()
                        )
                if amount:
                    if amount != c.amount:
                        c = UTILS.update(c, 'amount', float(amount))
                    else:
                        return UTILS.api_response(
                            msg=UTILS.NO_CHANGE(
                                TYPE, f'{c.id} in fund {c.fund_id}'
                            ),
                            code=400,
                            data=Capitalcall.query
                            .get(capitalcall_id).to_json()
                        )
                if date:
                    c = UTILS.update(c, 'date', date)
                return UTILS.api_response(
                    msg=UTILS.UPDATED(TYPE, f'{c.id} in fund {c.fund_id}'),
                    code=202,
                    data=Capitalcall.query.get(capitalcall_id).to_json()
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, capitalcall_id),
                    code=405,
                )
        except exc.IntegrityError as e:
            db.session.rollback()
            return UTILS.api_response(
                msg=f'{UTILS.INTEGRITY_ERR} {self.__name__}',
                code=405,
                data=f'{str(e)}'
            )

    def delete(self, capitalcall_id):
        """Delete single capitalcall details"""
        try:
            capitalcall = Capitalcall.query \
                            .filter_by(id=int(capitalcall_id)) \
                            .first()
            if not capitalcall:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, capitalcall_id),
                    code=404,
                )
            else:
                UTILS.delete(capitalcall)
                return UTILS.api_response(
                    msg=UTILS.DELETED(TYPE, capitalcall.id),
                    code=200
                )
        except ValueError as e:
            return UTILS.api_response(
                msg=f'{UTILS.VALUE_ERR} {self.__name__}',
                code=404,
                data=f'{str(e)}'
            )


api.add_resource(CapitalcallsPing, '/capitalcalls/ping')
api.add_resource(CapitalcallsList, '/capitalcalls')
api.add_resource(Capitalcalls, '/capitalcalls/<capitalcall_id>')
