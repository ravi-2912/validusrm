from flask import request
from sqlalchemy import exc
from flask_restful import Resource

from api import db
from api.capital_call import api
from api.capital_call.models import Committment
import api.capital_call.utils as UTILS


TYPE = 'Committment'


class CommittmentsPing(Resource):
    __name__ = 'CommittmentsPing'

    def get(self):
        return UTILS.api_response(
            msg=UTILS.PING_SUCCESS,
            code=200,
            data=self.__name__
        )


class CommittmentsList(Resource):
    __name__ = 'CommittmentsList'

    def get(self):
        """Get all committments"""
        committments = Committment.query.all()
        return UTILS.api_response(
            msg=UTILS.YES_FUNDSLIST if committments else UTILS.NO_FUNDSLIST,
            code=200,
            data={'committments': [c.to_json() for c in committments]}
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
            committment = UTILS.add_committment(fund_id, amount)
            return UTILS.api_response(
                msg=UTILS.ADDED(TYPE, amount),
                code=201,
                data=committment.to_json()
                )
        except exc.IntegrityError as e:
            db.session.rollback()
            return UTILS.api_response(
                msg=f'{UTILS.INTEGRITY_ERR} {self.__name__}',
                code=400,
                data=f'{str(e)}'
            )


api.add_resource(CommittmentsPing, '/committments/ping')
api.add_resource(CommittmentsList, '/committments')
