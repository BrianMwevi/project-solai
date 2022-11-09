from django.urls import re_path
from stocks_sockets import consumers


websocket_urlpatterns = [
    re_path(r'ws/stocks/realtime/$', consumers.StockConsumer.as_asgi()),
]
