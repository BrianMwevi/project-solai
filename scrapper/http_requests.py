import json
from decouple import config
from aiohttp import ClientSession


def get_url():
    api_url = f"{config('PROD_URL')}/realtime/admin/"
    return api_url


async def create_stocks(create_list):
    custom_print(f"Creating: {len(create_list)} stock(s)...")
    url = get_url()
    data = {"stocks": create_list}
    async with ClientSession() as session:
        stocks = await fetch_url(url, 'POST', session, data)
        custom_print(f"Created: {len(stocks['stocks'])} stock(s)\n")
        return stocks


async def update_stocks(update_list):
    custom_print(f"Updating: {len(update_list)} stock(s)...")
    url = get_url()
    data = {"stocks": update_list}
    async with ClientSession() as session:
        stocks = await fetch_url(url, 'PUT', session, data)
        custom_print(f"Updated: {len(stocks['stocks'])} stock(s)\n")
        return stocks


async def fetch_url(url: str, method: str, session: ClientSession, data, **kwargs):
    resp = await session.request(method=method, url=url, json=data, **kwargs)
    resp.raise_for_status()
    return json.loads(await resp.text())


def custom_print(text):
    print(f"\n::: {text}", end="")
