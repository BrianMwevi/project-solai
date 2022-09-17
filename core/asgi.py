import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django_asgi_app = get_asgi_application()

import stocks_channel.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(
    #     stocks_channel.routing.websocket_urlpatterns
    # )))
    "websocket": URLRouter(
        stocks_channel.routing.websocket_urlpatterns
    )
})
