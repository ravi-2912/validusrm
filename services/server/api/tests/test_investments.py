import json
import unittest
from datetime import datetime

from api.tests.base import BaseTestCase
import api.capital_call.utils as UTILS


TYPE = 'Investments'


class TestInvestmentsService(BaseTestCase):
    """Tests for the Investment Service."""
    def setUp(self):
        super().setUp()
        self.fund_1 = UTILS.add_fund('fund_1')
        self.fund_2 = UTILS.add_fund('fund_2')
        self.fund_3 = UTILS.add_fund('fund_3')
        self.fund_4 = UTILS.add_fund('fund_4')
        self.fund_5 = UTILS.add_fund('fund_5')
        self.committment_1 = UTILS.add_committment(
            1, 1000, datetime.strptime('31/12/2017', '%d/%m/%Y')
        )
        self.committment_2 = UTILS.add_committment(
            2, 1500, datetime.strptime('31/03/2018', '%d/%m/%Y')
        )
        self.committment_3 = UTILS.add_committment(
            3, 1000, datetime.strptime('30/06/2018', '%d/%m/%Y')
        )
        self.committment_4 = UTILS.add_committment(
            4, 1500, datetime.strptime('30/09/2018', '%d/%m/%Y')
        )
        self.committment_5 = UTILS.add_committment(
            1, 1000, datetime.strptime('31/12/2018', '%d/%m/%Y')
        )
        self.capitalcall_1 = UTILS.add_capitalcall(
            'investment_1', 950,
            datetime.strptime('31/01/2018', '%d/%m/%Y')
        )
        self.capitalcall_2 = UTILS.add_capitalcall(
            'investment_2', 2000,
            datetime.strptime('30/04/2018', '%d/%m/%Y')
        )

    def test_add_investment(self):
        with self.client as client:
            response = client.post(
                '/investments',
                data=json.dumps({
                    'rule': 'fifo',
                    'call_id': 2
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(UTILS.ADDED(TYPE, f'for Capital Call ID 2'),
                          data['message'])
            self.assertIn('success', data['status'])
            self.assertEqual(2, len(data['data']['fundinvestments']))
            self.assertEqual(
                1, data['data']['fundinvestments'][0]['committment_id']
            )
            self.assertEqual(
                1, data['data']['fundinvestments'][0]['fund_id']
            )
            self.assertEqual(
                2, data['data']['fundinvestments'][1]['fund_id']
            )



if __name__ == '__main__':
    unittest.main()
