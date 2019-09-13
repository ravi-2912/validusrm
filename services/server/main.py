# Local testing file

import os
import click
import subprocess


# Set environment variable
os.environ['FLASK_ENV'] = 'development'
os.environ['DATABASE_URL'] = 'sqlite:///local_dev.db'
os.environ['DATABASE_TEST_URL'] = 'sqlite:///local_test.db'
os.environ['APP_SETTINGS'] = 'api.config.DevelopmentConfig'


@click.group()
def cli():
    pass


@click.command()
def cov():
    subprocess.run('python manage.py cov')


@click.command()
def test():
    subprocess.run('python manage.py test')


@click.command()
def run():
    subprocess.run('python manage.py recreate_db')
    subprocess.run('python manage.py seed_db')
    subprocess.run('python manage.py run')


cli.add_command(cov)
cli.add_command(test)
cli.add_command(run)


if __name__ == '__main__':
    cli()
