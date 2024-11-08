from .base import *


SECRET_KEY = 'django-insecure-l^2s*xig=m^-zl)fk8eukp4qse+fn6c$f4vsc6fhd=+4ocvel('

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kenet',
        'USER':'postgres',
        'PASSWORD':'k3n3t',
        'HOST':'localhost',
        'PORT':'5432'
    }
}
