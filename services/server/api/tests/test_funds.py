import json
import unittest

from api.tests.base import BaseTestCase
from api.capital_call.funds import Fund
from api import db


def add_fund(fundname):
    fund = Fund(fundname)
    db.session.add(fund)
    db.session.commit()
    return fund


class TestFundsService(BaseTestCase):
    """Tests for the Capital Call Service."""

    def test_funds_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/funds/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('fund!', data['message'])
        self.assertIn('success', data['status'])

    def test_all_funds(self):
        """Ensure get all funds behaves correctly."""
        fund1 = add_fund('fund_1')
        fund2 = add_fund('fund_2')
        with self.client as client:
            response = client.get('/funds')
            data = json.loads(response.data.decode())
            funds = data['data']['funds']
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(funds), 2)
            self.assertEqual(fund1.fundname, funds[0]['fundname'])
            self.assertEqual(fund2.fundname, funds[1]['fundname'])
            self.assertEqual([], funds[0]['committments'])
            self.assertEqual([], funds[1]['committments'])
            self.assertEqual([], funds[0]['fundinvestments'])
            self.assertEqual([], funds[1]['fundinvestments'])
            self.assertIn('success', data['status'])

    def test_add_fund(self):
        """Ensure a new fund can be added to the database."""
        with self.client as client:
            response = client.post(
                '/funds',
                data=json.dumps({
                    'fundname': 'fund_1',
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('fund_1 was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_fund_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client as client:
            response = client.post(
                '/funds',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_fund_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a fundname key.
        """
        with self.client as client:
            response = client.post(
                '/funds',
                data=json.dumps({'something': 'fund_!'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_fund_duplicate_name(self):
        """Ensure error is thrown if the fund already exists."""
        with self.client as client:
            client.post(
                '/funds',
                data=json.dumps({
                    'fundname': 'fund_1',
                }),
                content_type='application/json',
            )
            response = client.post(
                '/funds',
                data=json.dumps({
                    'fundname': 'fund_1',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That fund already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_fund(self):
        """Ensure get single fund behaves correctly."""
        fund = add_fund('fund_1')
        with self.client as client:
            response = client.get(f'/funds/{fund.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('fund_1', data['data']['fundname'])
            self.assertIn('success', data['status'])

    def test_single_fund_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client as client:
            response = client.get('/funds/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Fund does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_fund_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client as client:
            response = client.get('/funds/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Fund does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_update_fund(self):
        """Ensure a fund name can be updated in the database."""
        fund = add_fund('fund1')
        with self.client as client:
            response = client.put(
                f'/funds/{fund.id}',
                data=json.dumps({
                    'fundname': 'fund_1',
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertIn('fund1 was updated to fund_1!', data['message'])
            self.assertIn('success', data['status'])
            self.assertEqual(fund.id, data["data"]["id"])
            self.assertEqual('fund_1', data["data"]["fundname"])
            self.assertNotEqual('fund1', data["data"]["fundname"])

    def test_update_fund_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        fund = add_fund('fund_!')
        with self.client as client:
            response = client.put(
                f'/funds/{fund.id}',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])
            self.assertEqual(fund.id, data["data"]["id"])
            self.assertEqual('fund_!', data["data"]["fundname"])
            self.assertNotEqual('fund_1', data["data"]["fundname"])

    def test_update_fund_duplicate_name(self):
        """Ensure error is thrown if the updated fund already exists."""
        add_fund("fund_1")
        fund_2 = add_fund("fund_!")
        with self.client as client:
            response = client.put(
                f'/funds/{fund_2.id}',
                data=json.dumps({
                    'fundname': 'fund_1',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn('Sorry. That fund already exists.', data['message'])
            self.assertIn('fail', data['status'])
            self.assertEqual(fund_2.id, data["data"]["id"])
            self.assertEqual('fund_!', data["data"]["fundname"])
            self.assertNotEqual('fund_2', data["data"]["fundname"])

    def test_update_fund_incorrect_id(self):
        """Ensure error is thrown if the id is incorrect for updating fund."""
        add_fund("fund!")
        with self.client as client:
            response = client.put(
                '/funds/999',
                data=json.dumps({
                    'fundname': 'fund_1',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn('Sorry. That fund does not exist', data['message'])
            self.assertIn('fail', data['status'])
            self.assertFalse(data['data'])

    def test_update_fund_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        add_fund("fund!")
        with self.client as client:
            response = client.put(
                '/funds/blah',
                data=json.dumps({
                    'fundname': 'fund_1',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn('Sorry. That fund does not exists.', data['message'])
            self.assertIn('fail', data['status'])
            self.assertFalse(data['data'])

    def test_update_fund_no_change(self):
        """Ensure correct response recieved for no change to updated fund"""
        fund = add_fund('fund_1')
        with self.client as client:
            response = client.put(
                f'/funds/{fund.id}',
                data=json.dumps({
                    'fundname': 'fund_1',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn('Sorry. That fund already exists', data['message'])

    def test_delete_fund(self):
        """Ensure fund is deleted"""
        fund = add_fund('fund_1')
        with self.client as client:
            res = client.delete(f'/funds/{fund.id}')
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn(f'{fund.fundname} successfully deleted.',
                          data['message'])


if __name__ == '__main__':
    unittest.main()
