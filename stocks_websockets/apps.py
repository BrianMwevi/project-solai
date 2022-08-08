from django.apps import AppConfig
import asyncio
from stocks_websockets.app import stocks_sock


class StocksWebsocketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stocks_websockets'
    def ready(self) -> None:
        asyncio.run(stocks_sock())
