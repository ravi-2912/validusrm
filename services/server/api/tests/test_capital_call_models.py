from sqlalchemy.exc import IntegrityError

from api.tests.base import BaseTestCase
from api.tests.base import db
from api.capital_call.models import Fund, Committment


class TestFundModel(BaseTestCase):
    def test_add_fund(self):
        """Test to commit a new fund to database"""
        fund = Fund(fundname='test_fund')
        db.session.add(fund)
        db.session.commit()
        self.assertTrue(fund.id)
        self.assertEqual(fund.fundname, 'test_fund')

    def test_to_json(self):
        """Test to to check if fund JSON is recieved as dict"""
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


class TestCommittmentModel(BaseTestCase):
    def test_add_committment(self):
        """Test to commit a new committment to database"""
        fund = Fund(fundname='test_fund')
        db.session.add(fund)
        db.session.commit()
        committment = Committment(
            fund_id=fund.id,
            amount=1000
        )
        db.session.add(committment)
        db.session.commit()
        self.assertTrue(committment.id)
        self.assertEqual(committment.amount, 1000)
        self.assertEqual(committment.fund_id, fund.id)

    def test_to_json(self):
        """Test to to check if committment JSON is recieved as dict"""
        committment = Committment(
            fund_id=1,
            amount=1000
        )
        db.session.add(committment)
        db.session.commit()
        self.assertTrue(isinstance(committment.to_json(), dict))

    def test_check_committent_from_fund(self):
        """Test to check that Fund & Committment relationship work"""
        fund = Fund(fundname='test_fund')
        db.session.add(fund)
        db.session.commit()
        committment = Committment(
            fund_id=fund.id,
            amount=1000
        )
        db.session.add(committment)
        db.session.commit()
        self.assertTrue(fund.committments)
        self.assertTrue(hasattr(fund.committments, '__iter__'))
        self.assertTrue(isinstance(fund.committments[0], Committment))
        self.assertEqual(committment.id, fund.committments[0].id)

    def test_add_two_committments_from_same_fund(self):
        """Test to check that two committments with same fund are added"""
        fund = Fund(fundname='fund1')
        db.session.add(fund)
        db.session.commit()
        committment1 = Committment(
            fund_id=fund.id,
            amount=1500
        )
        committment2 = Committment(
            fund_id=fund.id,
            amount=2500
        )
        db.session.add(committment1)
        db.session.add(committment2)
        db.session.commit()
        self.assertEqual(committment1.id, fund.committments[0].id)
        self.assertEqual(committment2.id, fund.committments[1].id)
        self.assertEqual(committment1.fund_id, committment2.fund_id)


class TestCapitalCallModel(BaseTestCase):
    def test_add_call(self):
        """Test to commit a new call to database"""
        call = CapitalCall(
            investment_name='invest_1',
            capital_requirement=1500
        )
        db.session.add(call)
        db.session.commit()
        self.assertTrue(call.id)
        self.assertEqual(call.investment_name, 'invest_1')
