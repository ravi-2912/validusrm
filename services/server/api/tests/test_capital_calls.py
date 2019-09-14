import json
import unittest

from api.tests.base import BaseTestCase
from api.capital_call.models import Fund, \
    Committment
from api import db


def add_fund(fundname):
    fund = Fund(fundname)
    db.session.add(fund)
    db.session.commit()
    return fund


def add_committment(fund_id, amount, date=None):
    committment = Committment(fund_id, amount, date)
    db.session.add(committment)
    db.session.commit()
    return committment


class TestCapitalCallService(BaseTestCase):
    """Tests for the Capital Call Service."""

    def test_funds_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/funds/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('fund!', data['message'])
        self.assertIn('success', data['status'])
    

if __name__ == '__main__':
    unittest.main()
