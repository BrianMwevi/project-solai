import json
from channels.generic.websocket import AsyncWebsocketConsumer
from updater.compare import get_stocks


class StockConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("stock_clients", self.channel_name)

        await self.accept()

        stocks = list(get_stocks().values())
        await self.send(text_data=json.dumps(stocks))

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            "stock_clients", self.channel_name)

    async def client_message(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
