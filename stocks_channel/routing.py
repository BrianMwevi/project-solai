from django.urls import re_path
from stocks_channel import consumers


websocket_urlpatterns = [
    re_path(r'ws/stocks/realtime/$', consumers.StockConsumer.as_asgi()),
    re_path(r'ws/stocks/history/$', consumers.HistoryConsumer.as_asgi()),
    re_path(r'ws/stocks/notifications/$',
            consumers.NotificationConsumer.as_asgi()),
]
