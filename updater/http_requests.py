import json
from decouple import config
from aiohttp import ClientSession


class StocksController:

    async def create_stocks(self, data):
        self.logger(f"Creating {len(data['stocks'])} stock(s)...")
        stocks = await self.send_request("POST", data, 'Created')
        return stocks

    async def update_stocks(self, data):
        self.logger(f"Updating {len(data['stocks'])} stock(s)...")
        stocks = await self.send_request("PUT", data, "Updated")
        return stocks

    async def send_request(self, method, data, operation):
        url = f"{config('PROD_URL')}/realtime/admin/"
        async with ClientSession() as session:
            resp = await session.request(method=method, url=url, json=data)
            resp.raise_for_status()
            stocks = json.loads(await resp.text())
            self.logger(
                f"{operation} {len(stocks['stocks'])} stock(s)\n")
            return stocks

    async def logger(text):
        print(f"\n::: {text}", end="")
