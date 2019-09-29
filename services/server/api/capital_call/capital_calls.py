from flask import request
from sqlalchemy import exc
from flask_restful import Resource
from datetime import datetime

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
            code=200 if calls else 404,
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
        name = post_data.get('name')
        capital = post_data.get('capital')
        date_str = post_data.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        try:
            call = CapitalCall.query \
                .filter_by(name=name) \
                .first()
            if not call:
                call_i = UTILS.add_capitalcall(
                    name, capital, date=date
                )
                return UTILS.api_response(
                    msg=UTILS.ADDED(TYPE, name),
                    code=201,
                    data=call_i.to_json()
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.EXISTS(TYPE, name),
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
                .filter_by(id=int(capitalcall_id)).first()
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
                code=400
            )
        name = put_data.get('name')
        capital = put_data.get('capital')
        try:
            call = CapitalCall.query.get(capitalcall_id)
            existingCalls = CapitalCall.query \
                .filter_by(name=name).first()
            if existingCalls:
                return UTILS.api_response(
                    msg=UTILS.EXISTS(TYPE, name),
                    code=400,
                    data=existingCalls.to_json()
                )
            if call:
                if (capital and (capital == call.capital)):
                    return UTILS.api_response(
                        msg=UTILS.NO_CHANGE(TYPE, f'{call.name}'),
                        code=400,
                        data=call.to_json()
                    )
                if name:
                    call = UTILS.update(call, 'name', name)
                if capital:
                    call = UTILS.update(call, 'capital', capital)
                return UTILS.api_response(
                    msg=UTILS.UPDATED(TYPE, name),
                    code=200,
                    data=CapitalCall.query.get(capitalcall_id).to_json()
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, capitalcall_id),
                    code=404,
                )
        except exc.IntegrityError as e:
            db.session.rollback()
            return UTILS.api_response(
                msg=f'{UTILS.INTEGRITY_ERR} {self.__name__}',
                code=400,
                data=f'{str(e)}'
            )

    def delete(self, capitalcall_id):
        """Delete single capitalcall details"""
        try:
            capitalcall = CapitalCall.query \
                .filter_by(id=int(capitalcall_id)).first()
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
