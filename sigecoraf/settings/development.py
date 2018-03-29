from .base import *
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sigecoraf',
        'USER': 'ronald',
        'PASSWORD': 'barcelona15',
        'HOST': 'localhost',
        'PORT': '5432',
    }

}
