# Local testing file

import os
import subprocess


# Set environment variable
os.environ['FLASK_ENV'] = 'development'
os.environ['APP_SETTINGS'] = 'api.config.DevelopmentConfig'
os.environ['DATABASE_URL'] = 'sqlite:///dev.db'


if __name__ == '__main__':
    subprocess.run('python manage.py recreate_db')
    subprocess.run('python manage.py cov')
    subprocess.run('python manage.py run')
