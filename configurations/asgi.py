import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import configurations.routing  # Import your routing configuration

# Set the settings module explicitly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configurations.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            configurations.routing.websocket_urlpatterns
        )
    ),
})
