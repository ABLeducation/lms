# from lms.wsgi import application
import sys
import os

# Set the project base directory
sys.path.insert(0, '/home/z28drb89ehvd/ablskool')

# Activate the virtual environment
activate_env = os.path.expanduser("/home/z28drb89ehvd/virtualenv/ablskool/3.10/bin/activate_this.py")
with open(activate_env) as f:
    exec(f.read(), dict(__file__=activate_env))

# Set the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'lms.settings'

# Import the application
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except ModuleNotFoundError as e:
    import logging
    logging.error(f"Module not found: {e}")
    raise

