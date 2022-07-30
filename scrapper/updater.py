from decouple import config
from aiohttp import ClientSession


async def update_stocks(update_list, create_list):
    api_url = f"{config('PROD_URL')}/realtime/admin/"
    if update_list:
        data = {"stocks": update_list}
        async with ClientSession() as session:
            await fetch_url(api_url, 'PUT', session, data)
    if create_list:
        data = {"stocks": create_list}
        async with ClientSession() as session:
            await fetch_url(api_url, 'POST', session, data)
    return True


async def fetch_url(url: str, method: str, session: ClientSession, data, **kwargs):
    resp = await session.request(method=method, url=url, json=data, **kwargs)
    resp.raise_for_status()
    stocks = await resp.text()
    return stocks
