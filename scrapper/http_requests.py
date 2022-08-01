import json
from decouple import config
from aiohttp import ClientSession


async def update_stocks(update_list, create_list):
    api_url = f"{config('PROD_URL')}/realtime/admin/"
    if update_list is not None:
        custom_print(f"Updating: {len(update_list)} stock(s)...")
        data = {"stocks": update_list}
        async with ClientSession() as session:
            stocks = await fetch_url(api_url, 'PUT', session, data)
            custom_print(f"Updated: {len(stocks['stocks'])} stock(s)\n")
    if create_list is not None:
        custom_print(f"Creating: {len(create_list)} stock(s)...")
        data = {"stocks": create_list}
        async with ClientSession() as session:
            stocks = await fetch_url(api_url, 'POST', session, data)
            custom_print(f"Created: {len(stocks['stocks'])} stock(s)\n")


async def fetch_url(url: str, method: str, session: ClientSession, data, **kwargs):
    resp = await session.request(method=method, url=url, json=data, **kwargs)
    resp.raise_for_status()
    stocks = await resp.text()
    return json.loads(stocks)


def custom_print(text):
    print(f"\n::: {text}", end="")
