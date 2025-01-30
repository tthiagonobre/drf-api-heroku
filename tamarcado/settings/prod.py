from tamarcado.settings.base import *

import os
from urllib.parse import urlparse

DATABASE_URL = os.getenv('DATABASE_URL')
url = urlparse(DATABASE_URL)

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': url.path[1:],  # Remove the leading slash from the DB name
         'USER': url.username,
         'PASSWORD': url.password,
         'HOST': url.hostname,
         'PORT': url.port,
    }
}