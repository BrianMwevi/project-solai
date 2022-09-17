import os
from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from stocks_channel import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django_asgi_app = get_asgi_application()

# import stocks_channel.routing

application = ProtocolTypeRouter({
    # "http": django_asgi_app,
    # "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(
    #     stocks_channel.routing.websocket_urlpatterns
    # )))
    "websocket": URLRouter([
        re_path(r'ws/stocks/realtime/$', consumers.StockConsumer.as_asgi()),

    ])
})
