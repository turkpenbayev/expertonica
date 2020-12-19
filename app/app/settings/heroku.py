import dj_database_url
import os
from .base import BASE_DIR, MIDDLEWARE, STATICFILES_STORAGE

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "dariya-su.herokuapp.com"]

MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES = {
    'default': {}
}
DATABASES['default'].update(db_from_env)