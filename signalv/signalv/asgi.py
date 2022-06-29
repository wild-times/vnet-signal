"""
ASGI config for signalv project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from chat.routing import websocket_urlpatterns as chat_routing_patterns
from sig.routing import websocket_urlpatterns as sig_routing_patterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'signalv.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter([*sig_routing_patterns, *chat_routing_patterns]))
})
