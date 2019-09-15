import sys
import unittest
from flask.cli import FlaskGroup

from testcoverage import COV
from api import create_app, db
from api.auth.users import User
from api.capital_call.funds import Fund


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
    db.session.add(Fund('fund_1'))
    db.session.add(Fund('fund_2'))
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    #tests = unittest.TestLoader().discover('api/tests', pattern='test_*.py')
    from api.tests.test_funds import TestFundsService
    tests = unittest.TestLoader().loadTestsFromTestCase(TestFundsService)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


if __name__ == '__main__':
    cli()
