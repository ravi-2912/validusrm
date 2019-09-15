from flask import request
from flask_restful import Resource
from sqlalchemy import exc

from api.capital_call.models import Fund
from api.capital_call import api
from api import db


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

    def post(self):
        post_data = request.get_json()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        if not post_data:
            return response_object, 400

        fundname = post_data.get('fundname')
        try:
            fund = Fund.query.filter_by(fundname=fundname).first()
            if not fund:
                db.session.add(Fund(fundname))
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': f'{fundname} was added!'
                }
                return response_object, 201
            else:
                response_object['message'] = 'Sorry. ' \
                    'That fund already exists.'
                return response_object, 400
        except exc.IntegrityError:
            db.session.rollback()
            return response_object, 400


class Funds(Resource):
    def get(self, fund_id):
        """Get single fund details"""
        response_object = {
            'status': 'fail',
            'message': 'Fund does not exist'
        }
        try:
            fund = Fund.query.filter_by(id=int(fund_id)).first()
            if not fund:
                return response_object, 404
            else:
                response_object = {
                    'status': 'success',
                    'data': fund.to_json()
                }
                return response_object, 200
        except ValueError:
            return response_object, 404

    def put(self, fund_id):
        put_data = request.get_json()
        try:
            fund = Fund.query.get(fund_id)
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload.',
                'data': fund.to_json() if fund else []
            }
            if not put_data:
                return response_object, 405

            fundname = put_data.get('fundname')
            existingFunds = Fund.query.filter_by(fundname=fundname).all()
            if not existingFunds:
                if fund:
                    oldfundname = fund.fundname
                    fund.fundname = fundname
                    db.session.commit()
                    response_object = {
                        'status': 'success',
                        'message': f'{oldfundname} was updated to '
                                   f'{fundname}!',
                        'data': Fund.query.get(fund_id).to_json()
                    }
                    return response_object, 202
                else:
                    response_object['message'] = 'Sorry. ' \
                        'That fund does not exists.'
                    return response_object, 405
            else:
                response_object['message'] = 'Sorry. ' \
                    'That fund already exists.'
                return response_object, 405
        except exc.IntegrityError:
            db.session.rollback()
            return response_object, 405

    def delete(self, fund_id):
        """Delete single fund details"""
        response_object = {
            'status': 'fail',
            'message': 'Fund does not exist'
        }
        try:
            fund = Fund.query.filter_by(id=int(fund_id)).first()
            if not fund:
                return response_object, 404
            else:
                db.session.delete(fund)
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': f'{fund.fundname} successfully deleted.'
                }
                return response_object, 200
        except ValueError:
            return response_object, 404


api.add_resource(FundsPing, '/funds/ping')
api.add_resource(FundsList, '/funds')
api.add_resource(Funds, '/funds/<fund_id>')