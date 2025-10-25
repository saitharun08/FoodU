import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodu.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Handles traditional HTTP requests
    "http": django_asgi_app,

    # Handles WebSocket connections
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
