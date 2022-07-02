# from api.serializers import StockSerializer
import asyncio
from aiohttp import ClientSession
from datetime import datetime
from bs4 import BeautifulSoup
from decouple import config
# from api.serializers import StockSerializer


async def fetch_url(url: str, session: ClientSession, **kwargs):
    resp = await session.request(method='GET', url=url, **kwargs)
    resp.raise_for_status()
    xml_data = await resp.text()
    return xml_data


