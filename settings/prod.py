from .base import *


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