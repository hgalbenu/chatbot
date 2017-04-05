"""
WSGI config for chatbot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot.settings")

application = get_wsgi_application()
if settings.ENVIRONMENT == 'STAGING':
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(application)
