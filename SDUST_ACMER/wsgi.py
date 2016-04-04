"""
WSGI config for SDUST_ACMER project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import sys, os
from os.path import join, dirname, abspath

from django.core.wsgi import get_wsgi_application

PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0,PROJECT_DIR)

os.environ["DJANGO_SETTINGS_MODULE"] = "SDUST_ACMER.settings"

application = get_wsgi_application()
