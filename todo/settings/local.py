import os

from .base import *

DEBUG = True
SECRET_KEY = '@hgnm12&32i=ip_etvw4v+bx-zik@fwyv2_%drf3&5g41m@oy2'
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'local.sqlite3',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
