# settings.py

import os

environment = os.getenv('DJANGO_ENV', 'development')
if environment == 'production':
    from .settings.production import *
else:
    from .settings.development import *
