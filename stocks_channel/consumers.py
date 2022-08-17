# chat/consumers.py
from ipaddress import ip_address
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from scrapper.updater import get_stocks


class StockConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("stock_clients", self.channel_name)
        await self.accept()

        stocks = get_stocks()
        await self.send(text_data=json.dumps(list(stocks.values())))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            "stock_clients", self.channel_name)

    async def client_message(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
