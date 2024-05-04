# Using basic password hasher in order to speedup tests.
# In my tests, it takes 14microseconds to set the password for a single user using md5 and more than 150k microseconds
# using the default hasher
import typing

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS: list[typing.Any] = []
