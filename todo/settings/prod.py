import os

from .base import *

#DEBUG = True
#SECRET_KEY = '@hgnm12&32i=ip_etvw4v+bx-zik@fwyv2_%drf3&5g41m@oy2'
#ALLOWED_HOSTS = []

DEBUG = os.environ.get('DEBUG')
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'prod.sqlite3',
    }
}


STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = 'AKIAZ5J64XOHZGFWOIF3'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'djangotodoapi'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'


STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
