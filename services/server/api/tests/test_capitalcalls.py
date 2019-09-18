import json
import unittest

from api.tests.base import BaseTestCase
import api.capital_call.utils as UTILS

TYPE = 'CapitalCall'


class TestCapitalCallsService(BaseTestCase):
    """Tests for the Capital Call Service."""

    def test_capitalcalls_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/capitalcalls/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn(UTILS.PING_SUCCESS, data['message'])
        self.assertIn('success', data['status'])

    def test_all_capitalcalls(self):
        """Ensure get all capitalcalls behaves correctly."""
        call1 = UTILS.add_capitalcall('invest1', 1000)
        call2 = UTILS.add_capitalcall('invest2', 2000)
        with self.client as client:
            response = client.get('/capitalcalls')
            data = json.loads(response.data.decode())
            calls = data['data']['capitalcalls']
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(calls), 2)
            self.assertEqual(call1.investment_name, calls[0]['investment_name'])
            self.assertEqual(call2.investment_name, calls[1]['investment_name'])
            self.assertEqual([], calls[0]['fundinvestments'])
            self.assertEqual([], calls[1]['fundinvestments'])
            self.assertIn('success', data['status'])

    def test_add_capitalcall(self):
        """Ensure a new capitalcall can be added to the database."""
        with self.client as client:
            response = client.post(
                '/capitalcalls',
                data=json.dumps({
                    'investment_name': 'investment_1',
                    'capital_requirement': 2000
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(UTILS.ADDED(TYPE, 'investment_1'), data['message'])
            self.assertIn('success', data['status'])

    def test_add_capitalcall_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client as client:
            response = client.post(
                '/capitalcalls',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(UTILS.INVALID_PAYLD, data['message'])
            self.assertIn('fail', data['status'])

    def test_add_capitalcall_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a valid key.
        """
        with self.client as client:
            response = client.post(
                '/capitalcalls',
                data=json.dumps({'something': 'capitalcall_!'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(f'{UTILS.INTEGRITY_ERR} {TYPE}s', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_capitalcall_duplicate_name(self):
        """Ensure error is thrown if the capitalcall already exists."""
        with self.client as client:
            client.post(
                '/capitalcalls',
                data=json.dumps({
                    'investment_name': 'investment_1',
                    'capital_requirement': 1000
                }),
                content_type='application/json',
            )
            response = client.post(
                '/capitalcalls',
                data=json.dumps({
                    'investment_name': 'investment_1',
                    'capital_requirement': 2000
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                f'{UTILS.EXISTS(TYPE, "investment_1")}', data['message']
            )
            self.assertIn('fail', data['status'])

    def test_single_capitalcall(self):
        """Ensure get single capitalcall behaves correctly."""
        capitalcall = UTILS.add_capitalcall('investment_1', 1000)
        with self.client as client:
            response = client.get(f'/capitalcalls/{capitalcall.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('investment_1', data['data']['investment_name'])
            self.assertIn('success', data['status'])

    def test_single_capitalcall_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client as client:
            response = client.get('/capitalcalls/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn(f'{UTILS.VALUE_ERR} CapitalCalls', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_capitalcall_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client as client:
            response = client.get('/capitalcalls/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn(f'{UTILS.NOT_EXISTS(TYPE, "999")}',
                          data['message'])
            self.assertIn('fail', data['status'])

    def test_update_capitalcall(self):
        """Ensure a capitalcall name can be updated in the database."""
        capitalcall = UTILS.add_capitalcall('investment_!', 1000)
        with self.client as client:
            response = client.put(
                f'/capitalcalls/{capitalcall.id}',
                data=json.dumps({
                    'investment_name': 'investment_1'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertIn(UTILS.UPDATED(TYPE, 'investment_1'), data['message'])
            self.assertIn('success', data['status'])
            self.assertEqual(capitalcall.id, data["data"]["id"])
            self.assertEqual('investment_1', data["data"]["investment_name"])

    def test_update_capitalcall_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        capitalcall = UTILS.add_capitalcall('investment_1', 100)
        with self.client as client:
            response = client.put(
                f'/capitalcalls/{capitalcall.id}',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn(UTILS.INVALID_PAYLD, data['message'])
            self.assertIn('fail', data['status'])
            self.assertFalse(data['data'])

    def test_update_capitalcall_duplicate_name(self):
        """Ensure error is thrown if the updated capitalcall already exists."""
        capitalcall_1 = UTILS.add_capitalcall('investment_1', 100)
        capitalcall_2 = UTILS.add_capitalcall('investment_2', 100)
        with self.client as client:
            response = client.put(
                f'/capitalcalls/{capitalcall_2.id}',
                data=json.dumps({
                    'investment_name': 'investment_1'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn(
                UTILS.NO_CHANGE(TYPE, 'investment_1'), data['message']
            )
            self.assertIn('fail', data['status'])
            self.assertEqual(capitalcall_1.id, data["data"]["id"])

    def test_update_capitalcall_incorrect_id(self):
        """
        Ensure error is thrown if the id is incorrect for updating capitalcall.
        """
        UTILS.add_capitalcall('investment_1', 1000)
        with self.client as client:
            response = client.put(
                '/capitalcalls/999',
                data=json.dumps({
                    'investment_name': 'investment_2'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn(UTILS.NOT_EXISTS(TYPE, '999'),
                          data['message'])
            self.assertIn('fail', data['status'])
            self.assertFalse(data['data'])

    def test_update_capitalcall_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        UTILS.add_capitalcall('investment_1', 100)
        with self.client as client:
            response = client.put(
                '/capitalcalls/blah',
                data=json.dumps({
                    'investment_name': 'investment_2'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn(UTILS.NOT_EXISTS(TYPE, 'blah'),
                          data['message'])
            self.assertIn('fail', data['status'])
            self.assertFalse(data['data'])

    def test_update_capitalcall_no_change(self):
        """
        Ensure correct response recieved for no change to updated capitalcall
        """
        capitalcall = UTILS.add_capitalcall('investment_1', 1000)
        with self.client as client:
            response = client.put(
                f'/capitalcalls/{capitalcall.id}',
                data=json.dumps({
                    'investment_name': 'investment_1'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn(
                UTILS.NO_CHANGE(TYPE, 'investment_1'), data['message']
            )

    def test_delete_capitalcall(self):
        """Ensure capitalcall is deleted"""
        capitalcall = UTILS.add_capitalcall('investment_1', 1000)
        with self.client as client:
            res = client.delete(f'/capitalcalls/{capitalcall.id}')
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn(UTILS.DELETED(TYPE, capitalcall.id),
                          data['message'])


if __name__ == '__main__':
    unittest.main()
