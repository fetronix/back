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

STATIC_URL = 'static/'
# The directory where static files are collected
STATIC_ROOT = BASE_DIR / 'staticfiles'  # This is where static files will be collected
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Additional static files
    # You can add more directories here
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Media settings



STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # Optional


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
