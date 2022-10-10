import os
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from stocks_channel.userAuthMiddleware import UserAuthMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
import stocks_channel.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": UserAuthMiddleware(URLRouter(
        stocks_channel.routing.websocket_urlpatterns
    ))
})
