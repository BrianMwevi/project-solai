import json
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from updater.compare import get_stocks
from channels.db import database_sync_to_async
from stocks_v1.models import Stock, StockTracker
from api.serializers import StockSerializer
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync

# TODO: Create Authentication consumer using JWT


class StockConsumer(AsyncWebsocketConsumer):
    """Handles connections for unauthenticated users/clients"""
    async def connect(self):
        await self.accept()
        user = self.scope['user']

        if user.is_authenticated:
            await self.add_to_group()
            stocks = list(get_stocks().values())
            await self.send(text_data=json.dumps(stocks[:5]))
        else:
            stocks = list(get_stocks().values())
            await self.send(text_data=json.dumps(stocks))
            await self.channel_layer.group_add("stock_clients", self.channel_name)

    async def disconnect(self, code):
        await self.remove_from_group()

    async def client_message(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def notification(self, event):
        data = event['data']
        return await self.send(text_data=data)

    @database_sync_to_async
    def remove_from_group(self):
        trackers = self.scope['user'].trackers.all()
        [async_to_sync(self.channel_layer.group_discard)(
            f"{tracker.stock.ticker}{tracker.quote_price}", self.channel_name)for tracker in trackers]

    @database_sync_to_async
    def add_to_group(self):
        trackers = self.scope['user'].trackers.all()
        [async_to_sync(self.channel_layer.group_add)(
            f"{tracker.stock.ticker}{tracker.quote_price}", self.channel_name)for tracker in trackers]


# TODO: Move notifications code to Notificatin class
class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """Handles websocket connections for authenticated users/clients and sends notifications"""

    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            return await self.close()

        await self.accept()
        await self.channel_layer.group_add("stock_users", self.channel_name)

    # TODO: Add receive method when user opens a notification
    async def disconnect(self, code):
        await self.channel_layer.group_discard("stock_users", self.channel_name)

    async def send_notification(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))


class HistoryConsumer(AsyncWebsocketConsumer):
    """Handles requests for historical data of a specific stock"""

    async def connect(self):
        if self.scope['user'].is_authenticated:
            await self.accept()
        else:
            # TODO:
            # await self.close() # uncomment this line to enable user auth
            await self.accept()  # remove this line to enable user auth

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        ticker = text_data_json['ticker'].upper()
        data = await self.get_history(ticker)
        await self.send(text_data=json.dumps(data))

    @ database_sync_to_async
    def get_history(self, ticker):
        serializer = StockSerializer(Stock.get_history(ticker), many=True)
        return {'data': serializer.data}
