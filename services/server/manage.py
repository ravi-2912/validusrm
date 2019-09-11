import os, sys, unittest, coverage
from flask.cli import FlaskGroup
from api import create_app, db
from api.auth.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

COV = coverage.coverage(
    branch=True,
    include='api/*',
    omit=[
        'api/tests/*',
        'api/config.py',
    ]
)
COV.start()


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('api/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('api/tests', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


if __name__ == '__main__':
    cli()