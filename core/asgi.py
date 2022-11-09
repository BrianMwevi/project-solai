from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django_asgi_app = get_asgi_application()

import stocks_sockets.routing
from stocks_sockets.userAuthMiddleware import UserAuthMiddleware


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": UserAuthMiddleware(URLRouter(
        stocks_sockets.routing.websocket_urlpatterns
    ))
})
