# -*- coding: utf-8 -*-
'''
Local Configurations
'''
from base import *

# DEBUG
DEBUG = True
TEMPLATE_DEBUG = DEBUG
# END DEBUG

# INSTALLED_APPS
INSTALLED_APPS = INSTALLED_APPS
# END INSTALLED_APPS

# Mail settings
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# End mail settings

# django-debug-toolbar
# MIDDLEWARE_CLASSES += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ]
# INSTALLED_APPS += [
#     'debug_toolbar',
# ]

INTERNAL_IPS = [
    '127.0.0.1',
    '10.0.2.2',
]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}
# end django-debug-toolbar

# Your local stuff: Below this line define 3rd party libary settings
