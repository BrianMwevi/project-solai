import json
from decouple import config
from aiohttp import ClientSession
from channels.layers import get_channel_layer


def get_url():
    api_url = f"{config('PROD_URL')}/realtime/admin/"
    return api_url


async def fetch_data(url: str, method: str, session: ClientSession, data, **kwargs):
    resp = await session.request(method=method, url=url, json=data, **kwargs)
    resp.raise_for_status()
    return json.loads(await resp.text())


async def create_stocks(create_list):
    custom_print(f"Creating: {len(create_list)} stock(s)...")
    url = get_url()
    data = {"stocks": create_list}
    async with ClientSession() as session:
        stocks = await fetch_data(url, 'POST', session, data)
        custom_print(f"Created: {len(stocks['stocks'])} stock(s)\n")
        return stocks


async def update_stocks(update_list):
    custom_print(f"Updating: {len(update_list)} stock(s)...")
    url = get_url()
    data = {"stocks": update_list}
    async with ClientSession() as session:
        stocks = await fetch_data(url, 'PUT', session, data)
        custom_print(f"Updated: {len(stocks['stocks'])} stock(s)\n")
        return stocks


async def update_clients(stock):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        'stock_clients',
        {
            'type': 'client_message',
            'data': stock,
        }
    )


def custom_print(text):
    print(f"\n::: {text}", end="")
