from .base import *
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sigecoraf',
        'USER': 'jorge.malla',
        'PASSWORD': '160190jorge',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
