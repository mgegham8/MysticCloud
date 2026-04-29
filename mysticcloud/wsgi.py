"""
WSGI config for mysticcloud project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'mysticcloud' project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysticcloud.settings')

# This is the application object used by Gunicorn to serve the project.
application = get_wsgi_application()