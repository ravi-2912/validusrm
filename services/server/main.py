## Local testing file

import os, subprocess

# Set environment variable
os.environ['FLASK_APP'] = r'services\server\api\__init__.py'
os.environ['FLASK_ENV'] = 'development'
os.environ['APP_SETTINGS'] = 'api.config.DevelopmentConfig'

subprocess.run('python manage.py run')

