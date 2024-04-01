# This file is alternative to active.py (although you can import it from there)
# The idea is to provide a way to import settings from the environment variables
# rather than having them hardcoded in active.py. This can allow easy setup of
# environments for docker launching
from enum import Enum

import environ

env = environ.Env()
environ.Env.read_env()


class Environments(Enum):
    PRODUCTION = 'PRODUCTION'
    DEV = 'DEV'


environment_name = env.str('ENVIRONMENT', '').upper()

if environment_name == Environments.PRODUCTION.value:
    ENVIRONMENT = Environments.PRODUCTION
    # noinspection PyUnresolvedReferences
    from schedulit.settings.prod import *
else:
    # Ignoring invalid environment names and defaulting to dev
    ENVIRONMENT = Environments.DEV
    # noinspection PyUnresolvedReferences
    from schedulit.settings.dev import *

if env.str('SECRET_KEY', None):
    SECRET_KEY = env.str('SECRET_KEY')

if env.str('DEBUG', None):
    DEBUG = env.bool('DEBUG')

if env.str('DATABASE_URL', None):
    DATABASES = {
        # DATABASE_URL format: postgres://<username>:<password>@<host>:<format>/<db name>
        'default': env.db('DATABASE_URL')
    }
elif env.str('RDS_HOSTNAME', None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env.str('RDS_DB_NAME', ''),
            'USER': env.str('RDS_USERNAME', ''),
            'PASSWORD': env.str('RDS_PASSWORD', ''),
            'HOST': env.str('RDS_HOSTNAME', ''),
            'PORT': env.str('RDS_PORT', '')
        }
    }

if env.str('EMAIL_HOST_USER', None):
    EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', '')
if env.str('EMAIL_HOST_PASSWORD', None):
    EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')
