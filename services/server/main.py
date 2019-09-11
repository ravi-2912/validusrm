# Local testing file

import os
import subprocess

# Set environment variable
# os.environ['FLASK_APP'] = r'services\server\api\__init__.py'
os.environ['FLASK_ENV'] = 'development'
os.environ['APP_SETTINGS'] = 'api.config.DevelopmentConfig'
os.environ['DATABASE_URL'] = '''postgres://postgres:postgres
                                @server-db:5432/capital_call_dev
                             '''

subprocess.run('python manage.py cov')
print('\n\n')
subprocess.run('python manage.py run')
