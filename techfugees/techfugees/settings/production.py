# -*- coding: utf-8 -*-
'''
Production Configurations
'''

from .base import *


# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# INSTALLED_APPS
INSTALLED_APPS = Common.INSTALLED_APPS
# END INSTALLED_APPS

# SECRET KEY
SECRET_KEY = values.SecretValue()
# END SECRET KEY

# django-secure
INSTALLED_APPS += ("djangosecure", )

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
SECURE_FRAME_DENY = values.BooleanValue(True)
SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
SESSION_COOKIE_SECURE = values.BooleanValue(False)
SESSION_COOKIE_HTTPONLY = values.BooleanValue(True)
SECURE_SSL_REDIRECT = values.BooleanValue(True)
# end django-secure

# SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]
# END SITE CONFIGURATION

# INSTALLED_APPS += ("", )

# EMAIL
DEFAULT_FROM_EMAIL = values.Value('techfugees<noreply@techfugees-map.letoosh.com>')
EMAIL_HOST = values.Value('')
EMAIL_HOST_PASSWORD = values.SecretValue(environ_prefix="", environ_name="EMAIL_PASSWORD")
EMAIL_HOST_USER = values.SecretValue(environ_prefix="", environ_name="EMAIL_USERNAME")
EMAIL_PORT = values.IntegerValue(587, environ_prefix="", environ_name="EMAIL_PORT")
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER
# END EMAIL

# TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
# END TEMPLATE CONFIGURATION

# DATABASE STUFF

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'techfugees',
        'USER': 'techfugees',
        'PASSWORD': 'fhew423aok4212da95l1sn',
        'HOST': '',
        'PORT': '',
        'CONN_MAX_AGE': 300,
    }
}

DEFAULT_LOGGER_NAME = "techfugees"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'gelf': {
            'class': 'graypy.GELFHandler',
            'host': 'logs.letolab.com',
            'port': 12201,
            'filters': ['static_fields', "django_exc"]
        },
    },
    'filters': {
        'static_fields': {
            '()': 'logfilters.StaticFieldFilter',
            'fields': {
                'project': 'techfugees',
                'environment': 'production',
            },
        },
        'django_exc': {
            '()': 'logfilters.RequestFilter',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'gelf'],
            'level': 'DEBUG',
            'propagate': True,
        },
        DEFAULT_LOGGER_NAME: {
            'handlers': ["console", 'gelf'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

# Your production stuff: Below this line define 3rd party libary settings

# SENTRY
INSTALLED_APPS += ("raven.contrib.django.raven_compat", )
RAVEN_CONFIG = {
    'dsn': '',
}
