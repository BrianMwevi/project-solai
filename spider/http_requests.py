import json
from decouple import config
from aiohttp import ClientSession
from channels.layers import get_channel_layer


class StocksController:
    headers = {
        "Authorization": f"Api-Key {config('API_KEY')}",
    }
    url = f"{config('PROD_URL')}/stocks/realtime/"

    @classmethod
    async def create_stocks(cls, data):
        cls.logger(f"Creating {len(data['stocks'])} stock(s)...")
        stocks = await cls.send_request("POST", data, 'Created')
        return stocks

    @classmethod
    async def update_stocks(cls, data):
        cls.logger(f"Updating {len(data['stocks'])} stock(s)...")
        stocks = await cls.send_request("PUT", data, "Updated")
        return stocks

    @classmethod
    async def send_request(cls, method, data, operation, **kwargs):
        async with ClientSession() as session:
            resp = await session.request(method=method, url=cls.url, json=data, headers=cls.headers, **kwargs)
            resp.raise_for_status()
            stocks = json.loads(await resp.text())
            cls.logger(
                f"{operation} {len(stocks['stocks'])} stock(s)\n")
            return stocks

    async def update_clients(stock):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "clients",
            {"type": "client_message", "data": stock}
        )

    def logger(text):
        return print(f"\n::: {text}", end="")
