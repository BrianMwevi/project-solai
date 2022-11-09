from channels.generic.websocket import AsyncWebsocketConsumer
import json
from updater.compare import get_stocks


class StockConsumer(AsyncWebsocketConsumer):
    """Handles realtime websocket connections for authenticated users"""

    async def connect(self):
        await self.accept()
        user = self.scope['user']

        if user.is_authenticated:
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
