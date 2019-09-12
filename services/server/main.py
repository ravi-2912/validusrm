# Local testing file

import os
import subprocess


# Set environment variable
os.environ['FLASK_ENV'] = 'development'
os.environ['DATABASE_URL'] = 'sqlite:///dev.db'
os.environ['DATABASE_TEST_URL'] = 'sqlite:///test.db'
os.environ['APP_SETTINGS'] = 'api.config.DevelopmentConfig'


if __name__ == '__main__':
    subprocess.run('python manage.py recreate_db')
    subprocess.run('python manage.py cov')
    
