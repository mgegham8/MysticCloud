"""
ASGI config for mysticcloud project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from django.core.asgi import get_asgi_application

# Set the default settings module for the 'mysticcloud' project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysticcloud.settings')

# The ASGI application is used for asynchronous features like WebSockets.
application = get_asgi_application()