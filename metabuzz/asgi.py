import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from interactions.routing import websocket_urlpatterns  # Ensure this import exists

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metabuzz.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
            interactions.routing.websocket_urlpatterns
    ),
})
