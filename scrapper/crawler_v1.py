import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from decouple import config
from asgiref.sync import sync_to_async
# from scraper.updater import update_stock

# from api.serializers import StockSerializer


async def fetch_url(url: str, session: ClientSession, **kwargs):
    resp = await session.request(method='GET', url=url, **kwargs)
    resp.raise_for_status()
    xml_data = await resp.text()
    print("Crawler")
    return xml_data


async def parse_data():
    """Converts string data to xml list of elements"""
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


async def process_ticker(element):
    stock = {}
    stock['ticker'] = element.get('a')
    price = stock['price'] = float(element.get('b').replace(',', ''))
    change = float(element.get('d')) if element.get('d') != None else 0
    change_direction = element.get('f')
    change = change*-1 if change_direction == 'l' else change
    open_price = stock['open_price'] = round(price - change, 2)
    stock['change'] = round(change*100/open_price, 2)
    return stock


async def update_local_db(stock):
    # update_stock(stock)
    pass


async def update_remote_db(stock):
    pass


async def main():
    ticker_elements = await parse_data()
    stocks = await process_data(ticker_elements)
    task1 = [asyncio.create_task(update_local_db(stock)) for stock in stocks]
    task2 = [asyncio.create_task(update_remote_db(stock)) for stock in stocks]


def scraper():
    asyncio.run(main())


scraper()
