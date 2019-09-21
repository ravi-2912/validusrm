import sys
import unittest
from flask.cli import FlaskGroup
from datetime import datetime

from testcoverage import COV
from api import create_app, db
from api.auth.users import User
from api.capital_call.funds import Fund
from api.capital_call.committments import Committment
from api.capital_call.capital_calls import CapitalCall
import api.capital_call.utils as UTILS


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('api/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('\n\nCoverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        print('\n\n')
        return 0
    sys.exit(result)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    db.session.add(User(username='ravi', email="ravi@gmail.com"))
    db.session.add(User(username='ravisingh', email="ravisingh@hotmail.org"))
    db.session.commit()
    fund_1 = UTILS.add_fund('fund_1')
    fund_2 = UTILS.add_fund('fund_2')
    fund_3 = UTILS.add_fund('fund_3')
    fund_4 = UTILS.add_fund('fund_4')
    fund_5 = UTILS.add_fund('fund_5')
    committment_1 = UTILS.add_committment(1, 10000000, datetime.
                          strptime('31/12/2017', '%d/%m/%Y'))
    committment_2 = UTILS.add_committment(2, 15000000, datetime.
                          strptime('31/03/2018', '%d/%m/%Y'))
    committment_3 = UTILS.add_committment(3, 10000000, datetime.
                          strptime('30/06/2018', '%d/%m/%Y'))
    committment_4 = UTILS.add_committment(4, 15000000, datetime.
                          strptime('30/09/2018', '%d/%m/%Y'))
    committment_5 = UTILS.add_committment(1, 10000000, datetime.
                          strptime('31/12/2018', '%d/%m/%Y'))
    
    capitalcall_1 = UTILS.add_capitalcall('investment_1', 9500000, datetime.
                          strptime('31/01/2018', '%d/%m/%Y'))
    capitalcall_2 = UTILS.add_capitalcall('investment_2', 10000000, datetime.
                          strptime('30/04/2018', '%d/%m/%Y'))
    
    UTILS.add_fundinvestment(9500000, fund_1, committment_1, capitalcall_1)
    UTILS.add_fundinvestment(500000, fund_1, committment_1, capitalcall_2)
    UTILS.add_fundinvestment(9500000, fund_2, committment_2, capitalcall_2)


@cli.command()
def test():
    """Runs the tests without code coverage"""
    #tests = unittest.TestLoader().discover('api/tests', pattern='test_*.py')
    from api.tests.test_capitalcalls import TestCapitalCallsService
    tests = unittest.TestLoader().loadTestsFromTestCase(TestCapitalCallsService)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


if __name__ == '__main__':
    cli()
