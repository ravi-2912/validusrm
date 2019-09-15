from flask import request
from sqlalchemy import exc
from flask_restful import Resource

from api import db
from api.capital_call import api
from api.capital_call.models import Fund
import api.capital_call.utils as UTILS


TYPE = 'Fund'


class FundsPing(Resource):
    __name__ = 'FundsPing'

    def get(self):
        return UTILS.api_response(
            msg=UTILS.PING_SUCCESS,
            code=200,
            data=self.__name__
        )


class FundsList(Resource):
    __name__ = 'FundsList'

    def get(self):
        """Get all funds"""
        funds = Fund.query.all()
        return UTILS.api_response(
            msg=UTILS.YES_FUNDSLIST if funds else UTILS.NO_FUNDSLIST,
            code=200,
            data={'funds': [fund.to_json() for fund in funds]}
        )

    def post(self):
        post_data = request.get_json()
        if not post_data:
            return UTILS.api_response(
                msg=UTILS.INVALID_PAYLD,
                code=400,
                data=self.__name__
            )
        fundname = post_data.get('fundname')
        try:
            fund = Fund.query.filter_by(fundname=fundname).first()
            if not fund:
                fund = UTILS.add_fund(fundname)
                return UTILS.api_response(
                    msg=UTILS.ADDED(TYPE, fundname),
                    code=201,
                    data=fund.to_json()
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.EXISTS(TYPE, fundname),
                    code=400,
                    data=fund.to_json()
                )
        except exc.IntegrityError as e:
            db.session.rollback()
            return UTILS.api_response(
                msg=f'{UTILS.INTEGRITY_ERR} {self.__name__}',
                code=400,
                data=f'{str(e)}'
            )


class Funds(Resource):
    __name__ = 'Funds'

    def get(self, fund_id):
        """Get single fund details"""
        try:
            fund = Fund.query.filter_by(id=int(fund_id)).first()
            if not fund:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, fund_id),
                    code=404,
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.EXISTS(TYPE, fund.id),
                    code=200,
                    data=fund.to_json()
                )
        except ValueError as e:
            return UTILS.api_response(
                msg=f'{UTILS.VALUE_ERR} {self.__name__}',
                code=404,
                data=f'{str(e)}'
            )

    def put(self, fund_id):
        put_data = request.get_json()
        fundname = put_data.get('fundname')
        if not put_data:
            return UTILS.api_response(
                msg=UTILS.INVALID_PAYLD,
                code=405
            )
        try:
            fund = Fund.query.get(fund_id)
            existingFunds = Fund.query.filter_by(fundname=fundname).first()
            if existingFunds:
                return UTILS.api_response(
                    msg=UTILS.EXISTS(TYPE, fundname),
                    code=405,
                    data=existingFunds.to_json()
                )
            if fund:
                fund = UTILS.update(fund, 'fundname', fundname)
                return UTILS.api_response(
                    msg=UTILS.UPDATED(TYPE, fundname),
                    code=202,
                    data=Fund.query.get(fund_id).to_json()
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, fund_id),
                    code=405,
                )
        except exc.IntegrityError as e:
            db.session.rollback()
            return UTILS.api_response(
                msg=f'{UTILS.INTEGRITY_ERR} {self.__name__}',
                code=405,
                data=f'{str(e)}'
            )

    def delete(self, fund_id):
        """Delete single fund details"""
        try:
            fund = Fund.query.filter_by(id=int(fund_id)).first()
            if not fund:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, fund_id),
                    code=404,
                )
            else:
                UTILS.delete(fund)
                return UTILS.api_response(
                    msg=UTILS.DELETED(TYPE, fund.id),
                    code=200
                )
        except ValueError as e:
            return UTILS.api_response(
                msg=f'{UTILS.VALUE_ERR} {self.__name__}',
                code=404,
                data=f'{str(e)}'
            )


api.add_resource(FundsPing, '/funds/ping')
api.add_resource(FundsList, '/funds')
api.add_resource(Funds, '/funds/<fund_id>')