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

# Redirecionamento automático para HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Segurança de Cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Clickjacking Protection
X_FRAME_OPTIONS = 'DENY'

# Referrer Policy
SECURE_REFERRER_POLICY = 'same-origin'
