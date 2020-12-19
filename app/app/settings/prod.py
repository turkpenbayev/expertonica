import os
from .base import BASE_DIR

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(0uqad7fcyv^7m2p0@i-0m5op&6t-z44dj@0@&udek09rn2z1u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', default=0))

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", os.environ.get('HOST_NAME')]


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('SQL_USER', 'user'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}