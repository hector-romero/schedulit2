import typing

DEBUG = True
SECRET_KEY = 'dev'

# Disable all password validation in dev, to make user creation simpler
AUTH_PASSWORD_VALIDATORS: list[typing.Any] = []
