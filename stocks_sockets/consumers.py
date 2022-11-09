from channels.generic.websocket import AsyncWebsocketConsumer
import json
from updater.compare import get_stocks
from drf_yasg.utils import swagger_auto_schema
from clock import market_is_open


class StockConsumer(AsyncWebsocketConsumer):
    """Handles realtime websocket connections for authenticated users"""

    @swagger_auto_schema(
        operation_description="Realtime stocks data",
        operation_summary="Gateway for clients to connected and receive realtime stocks data",
        operation_id="sockets",
        tags=["websockets"],

    )
    async def connect(self):
        market_open = market_is_open()

        if market_open and self.scope['user'].is_authenticated:
            await self.accept()
            stocks = list(get_stocks().values())
            await self.send(text_data=json.dumps(stocks))
            await self.channel_layer.group_add("clients", self.channel_name)
        else:
            await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("clients", self.channel_name)

    async def client_message(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
