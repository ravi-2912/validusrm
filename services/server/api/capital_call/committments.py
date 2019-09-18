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
            msg=(UTILS.YES_FUNDSLIST
                 if committments
                 else UTILS.NO_FUNDSLIST),
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
                msg=UTILS.ADDED(TYPE, f'{committment.id} in fund {fund_id}'),
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


class Committments(Resource):
    __name__ = 'Committments'

    def get(self, committment_id):
        """Get single committment details"""
        try:
            committment = Committment.query \
                            .filter_by(id=int(committment_id)) \
                            .first()
            if not committment:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, committment_id),
                    code=404,
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.SUCCESS(TYPE, committment.id),
                    code=200,
                    data=committment.to_json()
                )
        except ValueError as e:
            return UTILS.api_response(
                msg=f'{UTILS.VALUE_ERR} {self.__name__}',
                code=404,
                data=f'{str(e)}'
            )

    def put(self, committment_id):
        """Update single committment details"""
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
            c = Committment.query.get(committment_id)
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
                            data=c.query.get(committment_id).to_json()
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
                            data=Committment.query
                            .get(committment_id).to_json()
                        )
                if date:
                    c = UTILS.update(c, 'date', date)
                return UTILS.api_response(
                    msg=UTILS.UPDATED(TYPE, f'{c.id} in fund {c.fund_id}'),
                    code=202,
                    data=Committment.query.get(committment_id).to_json()
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, committment_id),
                    code=405,
                )
        except exc.IntegrityError as e:
            db.session.rollback()
            return UTILS.api_response(
                msg=f'{UTILS.INTEGRITY_ERR} {self.__name__}',
                code=405,
                data=f'{str(e)}'
            )

    def delete(self, committment_id):
        """Delete single committment details"""
        try:
            committment = Committment.query \
                            .filter_by(id=int(committment_id)) \
                            .first()
            if not committment:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, committment_id),
                    code=404,
                )
            else:
                UTILS.delete(committment)
                return UTILS.api_response(
                    msg=UTILS.DELETED(TYPE, committment.id),
                    code=200
                )
        except ValueError as e:
            return UTILS.api_response(
                msg=f'{UTILS.VALUE_ERR} {self.__name__}',
                code=404,
                data=f'{str(e)}'
            )


api.add_resource(CommittmentsPing, '/committments/ping')
api.add_resource(CommittmentsList, '/committments')
api.add_resource(Committments, '/committments/<committment_id>')
