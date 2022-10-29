from stocks_channel.userAuthMiddleware import UserAuthMiddleware
import stocks_channel.routing
from channels.routing import ProtocolTypeRouter, URLRouter
import os
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": UserAuthMiddleware(URLRouter(
        stocks_channel.routing.websocket_urlpatterns
    ))
})
