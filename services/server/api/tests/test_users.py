import json
import unittest
from api.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client as client:
            response = client.post(
                '/users',
                data=json.dumps({
                    'username': 'ravi',
                    'email': 'ravi@singh.com'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('ravi@singh.com was added!', data['message'])
            self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()