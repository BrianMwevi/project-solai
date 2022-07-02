# from api.serializers import StockSerializer
import asyncio
from aiohttp import ClientSession
from datetime import datetime
from bs4 import BeautifulSoup
from decouple import config
# from api.serializers import StockSerializer


async def fetch_url(url: str, session: ClientSession, **kwargs):
    print("Start: ", datetime.now())
    resp = await session.request(method='GET', url=url, **kwargs)
    resp.raise_for_status()
    xml_data = await resp.text()
    return xml_data


async def parse_data():
    async with ClientSession() as session:
        xml_data = await fetch_url(config("URL_V1"), session)
        soup = BeautifulSoup(xml_data, features="xml")
        return soup.select("i")


async def process_data(ticker_elements: list):
    async with ClientSession() as session:
        stocks = []
        for element in ticker_elements:
            if element.get('b') == "-":
                continue
            stocks.append(process_ticker(element))
        return await asyncio.gather(*stocks)

