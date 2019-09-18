import json
import unittest

from api.tests.base import BaseTestCase
import api.capital_call.utils as UTILS

TYPE = 'Committment'


class TestCommittmentsService(BaseTestCase):
    """Tests for the committments service."""

    def setUp(self):
        super().setUp()
        self.fund_1 = UTILS.add_fund('fund_1')
        self.fund_2 = UTILS.add_fund('fund_2')

    def test_committments_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/committments/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn(UTILS.PING_SUCCESS, data['message'])
        self.assertIn('success', data['status'])

    def test_all_committments(self):
        """Ensure get all committments behaves correctly."""
        committment1 = UTILS.add_committment(self.fund_1.id, 1000)
        committment2 = UTILS.add_committment(self.fund_2.id, 2000)
        with self.client as client:
            response = client.get('/committments')
            data = json.loads(response.data.decode())
            committments = data['data']['committments']
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(committments), 2)
            self.assertEqual(committment1.id, committments[0]['id'])
            self.assertEqual(committment2.id, committments[1]['id'])
            self.assertEqual(committment1.fund_id, committments[0]['fund_id'])
            self.assertEqual(committment2.fund_id, committments[1]['fund_id'])
            self.assertEqual(committment1.amount, committments[0]['amount'])
            self.assertEqual(committment2.amount, committments[1]['amount'])
            self.assertIn('success', data['status'])
            self.assertEqual(UTILS.YES_FUNDSLIST, data['message'])

    def test_add_committment(self):
        """Ensure a new committment can be added to the database."""
        with self.client as client:
            response = client.post(
                '/committments',
                data=json.dumps({
                    'fund_id': 1,
                    'amount': 1000
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(UTILS.ADDED(TYPE, f'1 in fund 1'), data['message'])
            self.assertEqual(1000, data['data']['amount'])
            self.assertIn('success', data['status'])

    def test_add_committment_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client as client:
            response = client.post(
                '/committments',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(UTILS.INVALID_PAYLD, data['message'])
            self.assertIn('fail', data['status'])

    def test_add_committment_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a fund_id key.
        """
        with self.client as client:
            response = client.post(
                '/committments',
                data=json.dumps({'amount': 100}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(f'{UTILS.INTEGRITY_ERR} {TYPE}s', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_committment_duplicate_name(self):
        """
        Ensure error is not thrown if the committment of dame fund_id already
        exists.
        """
        with self.client as client:
            client.post(
                '/committments',
                data=json.dumps({
                    'fund_id': 1,
                    'amount': 1000
                }),
                content_type='application/json',
            )
            response = client.post(
                '/committments',
                data=json.dumps({
                    'fund_id': 1,
                    'amount': 2000
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(UTILS.ADDED(TYPE, f'2 in fund 1'), data['message'])
            self.assertEqual(2000, data['data']['amount'])
            self.assertIn('success', data['status'])

    def test_single_committment(self):
        """Ensure get single committment behaves correctly."""
        committment = UTILS.add_committment(self.fund_1.id, 1000)
        with self.client as client:
            response = client.get(f'/committments/{committment.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(1000, data['data']['amount'])
            self.assertIn('success', data['status'])

    def test_single_committment_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client as client:
            response = client.get('/committments/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn(f'{UTILS.VALUE_ERR} {TYPE}s', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_committment_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client as client:
            response = client.get('/committments/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn(f'{UTILS.NOT_EXISTS(TYPE, "999")}',
                          data['message'])
            self.assertIn('fail', data['status'])

    def test_update_committment(self):
        """Ensure a committment amount can be updated in the database."""
        committment = UTILS.add_committment(self.fund_2.id, 2000)
        with self.client as client:
            response = client.put(
                f'/committments/{committment.id}',
                data=json.dumps({
                    'amount': 4000
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertIn(UTILS.UPDATED(TYPE,
                          f'{committment.id} in fund {self.fund_2.id}'),
                          data['message'])
            self.assertIn('success', data['status'])
            self.assertEqual(committment.id, data["data"]["id"])
            self.assertEqual(4000, data["data"]["amount"])

    def test_update_committment_incorrect_id(self):
        """
        Ensure error is thrown if the id is incorrect for updating committment.
        """
        UTILS.add_committment(self.fund_1.id, 1000)
        with self.client as client:
            response = client.put(
                '/committments/999',
                data=json.dumps({
                    'fund_id': '1',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn(UTILS.NOT_EXISTS(TYPE, '999'),
                          data['message'])
            self.assertIn('fail', data['status'])
            self.assertFalse(data['data'])

    def test_update_committment_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        UTILS.add_committment(self.fund_1.id, 1000)
        with self.client as client:
            response = client.put(
                '/committments/blah',
                data=json.dumps({
                    'fund_id': 1
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 405)
            self.assertIn(UTILS.NOT_EXISTS(TYPE, 'blah'),
                          data['message'])
            self.assertIn('fail', data['status'])
            self.assertFalse(data['data'])

    def test_update_committment_no_change(self):
        """
        Ensure correct response recieved for no change to updated committment
        """
        committment = UTILS.add_committment(self.fund_1.id, 1000)
        with self.client as client:
            response = client.put(
                f'/committments/{committment.id}',
                data=json.dumps({
                    'amount': 1000,
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                UTILS.NO_CHANGE(
                    TYPE,
                    f'{committment.id} in fund {committment.fund_id}'
                ),
                data['message']
            )

    def test_delete_committment(self):
        """Ensure committment is deleted"""
        committment = UTILS.add_committment(self.fund_1.id, 1000)
        with self.client as client:
            res = client.delete(f'/committments/{committment.id}')
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn(UTILS.DELETED(TYPE, committment.id),
                          data['message'])


if __name__ == '__main__':
    unittest.main()
