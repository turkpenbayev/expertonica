import os
from .base import BASE_DIR, ALLOWED_HOSTS, INSTALLED_APPS, MIDDLEWARE

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS += ["*"]


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


INTERNAL_IPS = [
    '127.0.0.1',
    'web-dev',
    'localhost'
]

def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}