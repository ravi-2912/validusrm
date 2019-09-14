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


api.add_resource(FundsPing, '/funds/ping')
