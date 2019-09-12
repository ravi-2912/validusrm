from flask import Blueprint, request
from flask_restful import Resource, Api
from api.auth.models import User
from api import db


auth_blueprint = Blueprint('users', __name__)
api = Api(auth_blueprint)


class UsersPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


class UsersList(Resource):
    def post(self):
        post_data = request.get_json()
        username = post_data.get('username')
        email = post_data.get('email')
        db.session.add(User(
                username=username,
                email=email
            )
        )
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'{email} was added!'
        }
        return response_object, 201


api.add_resource(UsersPing, '/users/ping')
api.add_resource(UsersList, '/users')
