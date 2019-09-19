# from flask import request
# from sqlalchemy import exc
from flask_restful import Resource

# from api import db
from api.capital_call import api
from api.capital_call.models import Investment, FundInvestments
import api.capital_call.utils as UTILS


TYPE = 'Investments'


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
        return UTILS.api_response(
            msg=UTILS.SUCCESS(TYPE, "")
            if investments else
            UTILS.NO_SUCCESS(TYPE, ""),
            code=200 if investments else 404,
            data={'investments': [i.to_json() for i in investments]}
        )

    def post(self):
        pass


class Investments(Resource):
    __name__ = 'Investments'

    def get(self, investment_id):
        """Get single investment details"""
        try:
            inv = Investment.query.filter_by(id=int(investment_id)).first()
            if not inv:
                return UTILS.api_response(
                    msg=UTILS.NOT_EXISTS(TYPE, investment_id),
                    code=404,
                )
            else:
                return UTILS.api_response(
                    msg=UTILS.SUCCESS(TYPE, inv.id),
                    code=200,
                    data=inv.to_json()
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
