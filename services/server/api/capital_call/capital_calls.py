from flask import request
from sqlalchemy import exc
from flask_restful import Resource

from api import db
from api.capital_call import api
from api.capital_call.models import CapitalCall
import api.capital_call.utils as UTILS


TYPE = 'CapitalCall'


class CapitalCallsPing(Resource):
    __name__ = 'CapitalcallsPing'

    def get(self):
        return UTILS.api_response(
            msg=UTILS.PING_SUCCESS,
            code=200,
            data=self.__name__
        )


class CapitalCallsList(Resource):
    __name__ = 'CapitalCallsList'

    def get(self):
        """Get all capitalcalls"""
        calls = CapitalCall.query.all()
        return UTILS.api_response(
            msg=(UTILS.SUCCESS(TYPE, "")
                 if calls
                 else UTILS.SUCCESS(TYPE, "")),
            code=200,
            data={'capitalcalls': [c.to_json() for c in calls]}
        )

    def post(self):
        post_data = request.get_json()
        if not post_data:
            return UTILS.api_response(
                msg=UTILS.INVALID_PAYLD,
                code=400,
                data=self.__name__
            )
        investment_name = post_data.get('investment_name')
        capital_requirement = post_data.get('capital_requirement')
        try:
            call = CapitalCall.query \
                .filter_by(investment_name=investment_name) \
                .first()
            if not call:
                call_i = UTILS.add_capitalcall(
                    investment_name, capital_requirement
                )
                return UTILS.api_response(
                    msg=UTILS.ADDED(TYPE, investment_name),
                    code=201,
                    data=call_i.to_json()
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.EXISTS(TYPE, investment_name),
                    code=400,
                    data=call.to_json()
                )
        except exc.IntegrityError as e:
            db.session.rollback()
            return UTILS.api_response(
                msg=f'{UTILS.INTEGRITY_ERR} {self.__name__}',
                code=400,
                data=f'{str(e)}'
            )


class CapitalCalls(Resource):
    __name__ = 'CapitalCalls'

    def get(self, capitalcall_id):
        """Get single capitalcall details"""
        try:
            call = CapitalCall.query \
                    .filter_by(id=int(capitalcall_id)) \
                    .first()
            if not call:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, capitalcall_id),
                    code=404,
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.SUCCESS(TYPE, call.id),
                    code=200,
                    data=call.to_json()
                )
        except ValueError as e:
            return UTILS.api_response(
                msg=f'{UTILS.VALUE_ERR} {self.__name__}',
                code=404,
                data=f'{str(e)}'
            )

    def put(self, capitalcall_id):
        put_data = request.get_json()
        if not put_data:
            return UTILS.api_response(
                msg=UTILS.INVALID_PAYLD,
                code=405
            )
        investment_name = put_data.get('investment_name')
        capital_requirement = put_data.get('capital_requirement')
        try:
            call = CapitalCall.query.get(capitalcall_id)
            existingCalls = CapitalCall.query \
                .filter_by(investment_name=investment_name) \
                .first()
            if existingCalls:
                return UTILS.api_response(
                    msg=UTILS.NO_CHANGE(TYPE, investment_name),
                    code=405,
                    data=existingCalls.to_json()
                )
            if call:
                if investment_name:
                    call = UTILS.update(
                        call, 'investment_name', investment_name
                    )
                if capital_requirement:
                    call = UTILS.update(
                        call, 'capital_requirement', capital_requirement
                    )
                return UTILS.api_response(
                    msg=UTILS.UPDATED(TYPE, investment_name),
                    code=202,
                    data=CapitalCall.query.get(capitalcall_id).to_json()
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
            capitalcall = CapitalCall.query \
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


api.add_resource(CapitalCallsPing, '/capitalcalls/ping')
api.add_resource(CapitalCallsList, '/capitalcalls')
api.add_resource(CapitalCalls, '/capitalcalls/<capitalcall_id>')
