## Local testing file

import os, subprocess

# Set environment variable
os.environ['FLASK_APP'] = r'services\server\api\__init__.py'
os.environ['FLASK_ENV'] = 'development'

subprocess.run('python manage.py run')

