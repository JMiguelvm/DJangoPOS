import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Usa solo HTTP por ahora
application = get_asgi_application()

# Deshabilitado websocket
"""
from channels.routing import ProtocolTypeRouter, URLRouter
from . import routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        routing.websocket_urlpatterns
    ),
})
"""