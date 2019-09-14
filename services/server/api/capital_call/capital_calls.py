from flask import Blueprint, request, render_template
from flask_restful import Resource, Api
from sqlalchemy import exc

from api.capital_call.models import Fund
from api import db


capital_call_blueprint = Blueprint(
    'capital_calls', __name__
)
api = Api(capital_call_blueprint)


class FundsPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'fund!'
        }


class FundsList(Resource):
    def get(self):
        """Get all funds"""
        response_object = {
            'status': 'success',
            'data': {
                'funds': [fund.to_json() for fund in Fund.query.all()]
            }
        }
        return response_object, 200


api.add_resource(FundsPing, '/funds/ping')
api.add_resource(FundsList, '/funds')
