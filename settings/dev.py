from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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