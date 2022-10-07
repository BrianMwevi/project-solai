import json
from channels.generic.websocket import AsyncWebsocketConsumer
from updater.compare import get_stocks

# TODO: Move notifications code to Notificatin class


class StockConsumer(AsyncWebsocketConsumer):
    """Handles connections for unauthenticated users/clients"""
    async def connect(self):
        await self.accept()
        user = self.scope['user']

        if user.is_authenticated:
            [await self.channel_layer.group_add(f"{tracker.ticker}{tracker.quote_price}") for tracker in user.trackers.all()]
            print("Trackers: ", user.trackers.all())
        else:
            await self.channel_layer.group_add("stock_clients", self.channel_name)
            stocks = list(get_stocks().values())
            await self.send(text_data=json.dumps(stocks))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            "stock_clients", self.channel_name)

    async def client_message(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def notification(self, event):
        data = event['data']
        return await self.send(text_data=data)


class NotificationConsumer(AsyncWebsocketConsumer):
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
