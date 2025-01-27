"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l^2s*xig=m^-zl)fk8eukp4qse+fn6c$f4vsc6fhd=+4ocvel('

# SECURITY WARNING: don't run with debug turned on in production!


DEBUG = False

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'livekenetdb',
        'USER': 'postgres',
        'PASSWORD': 'k3n3t',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'kenet',
#         'USER':'postgres',
#         'PASSWORD':'k3n3t',
#         'HOST':'localhost',
#         'PORT':'5432'
#     }
# }

STATIC_URL = 'static/'
# The directory where static files are collected
STATIC_ROOT = BASE_DIR / 'staticfiles'  # This is where static files will be collected
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Additional static files
    # You can add more directories here
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Media settings


# Email Configuration in settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Replace with your email provider's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'  # Use an environment variable for security
DEFAULT_FROM_EMAIL = 'Your App <your_email@example.com>'


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # Optional






# Application definition

INSTALLED_APPS = [
    # 'admin_interface',
    # 'colorfield',
    # 'grappelli',
    # 'djangocms_admin_style',
    "semantic_admin",
    "semantic_forms",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'background_task',

    'rest_framework', 
    'corsheaders',
    
    'KENETAssets.apps.KENETAssetsConfig',
    'version_control'

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Added WhiteNoise
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# SEMANTIC_APP_LIST = [
#     {
#         "app_label": "KENETAssets",
#         "models": [{"object_name": "Delivery"}, {"object_name": "Assets"}],
#     },
# ]

SEMANTIC_APP_LIST = [{ "app_label": "KENETAssets" },{ "app_label": "version_control" },{ "app_label": "background_task" }]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# # Ensure this is set
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
# )



# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'  # Set to Kenyan time
USE_I18N = True
USE_TZ = True

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


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# settings.py
AUTH_USER_MODEL = 'KENETAssets.CustomUser'  # Replace 'yourapp' with your actual app name


CORS_ALLOW_ALL_ORIGINS = True
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',
#     ],
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 1,  # Adjust this number to define the page size
    
}


from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

BACKGROUND_TASK_RUN_ASYNC = True