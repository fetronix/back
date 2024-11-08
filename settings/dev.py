from .base import *


DEBUG = True

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