import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metabuzz.settings')
django.setup()  # Ensure Django is fully loaded before importing anything

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notifications.routing
import direct_messages.routing


application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handle HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notifications.routing.websocket_urlpatterns +
            direct_messages.routing.websocket_urlpatterns
        )
    ),
})
