from flask import Blueprint
from flask_restful import Api

capital_call_blueprint = Blueprint(
    'capital_call', __name__
)

api = Api(capital_call_blueprint)
