from sqlalchemy.exc import IntegrityError

from api import db
from api.capital_call.models import Fund
from api.tests.base import BaseTestCase


class TestFundModel(BaseTestCase):
    def test_add_fund(self):
        """Test to commit a new fund to database"""
        fund = Fund(fundname='test_fund')
        db.session.add(fund)
        db.session.commit()
        self.assertTrue(fund.id)
        self.assertEqual(fund.fundname, 'test_fund')

    def test_to_json(self):
        """Test to to check is JSON is reciwved as dict"""
        fund = Fund(fundname='test_fund')
        db.session.add(fund)
        db.session.commit()
        self.assertTrue(isinstance(fund.to_json(), dict))

    def test_add_fund_duplicate_name(self):
        """Test to raise error on adding a duplicate fund name"""
        fund = Fund(fundname='test_fund')
        db.session.add(fund)
        db.session.commit()
        duplicate_fund = Fund(fundname='test_fund')
        db.session.add(duplicate_fund)
        self.assertRaises(IntegrityError, db.session.commit)
