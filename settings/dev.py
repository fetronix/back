from .base import *

SECRET_KEY = 'django-insecure-l^2s*xig=m^-zl)fk8eukp4qse+fn6c$f4vsc6fhd=+4ocvel('
DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

