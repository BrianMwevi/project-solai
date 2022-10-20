import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from decouple import config
from updater.http_requests import StocksController
from updater.compare import compare_stock, track_price


async def fetch(url: str, **kwargs):
    async with ClientSession() as session:
        resp = await session.request(method='GET', url=url, **kwargs)
        resp.raise_for_status()
        xml_data = await resp.text()
        return xml_data


async def parse_data(raw_data):
    async with ClientSession() as session:
        soup = BeautifulSoup(raw_data, features="xml")
        market_status = soup.select_one('mystocks').get('t')
        # TODO: Shutdown timer when market is closed
        # TODO: Update last stock history with close price
        # TODO: Do vice versa for when market is open
        print('closed' in str(market_status))
        return soup.select("i")


async def process_data(ticker_elements: list):
    async with ClientSession() as session:
        to_create = []
        to_update = []
        for element in ticker_elements:
            if element.get('b') == "-":
                continue
            stock = await process_ticker(element)
            updated, created = compare_stock(stock)
            if created:
                await StocksController.update_clients(created)
                to_create.append(created)
            if updated:
                await track_price(updated)
                await StocksController.update_clients(updated)
                to_update.append(updated)

        return ({"stocks": to_create}, {"stocks": to_update})


async def process_ticker(element):
    stock = {}
    stock['ticker'] = element.get('a')
    price = stock['price'] = float(element.get('b').replace(',', ''))
    change = float(element.get('d')) if element.get('d') != None else 0
    change_direction = element.get('f')
    change = change*-1 if change_direction == 'l' else change
    open_price = stock['open_price'] = round(price - change, 2)
    stock['percentage_change'] = round(change*100/open_price, 2)
    return stock


async def main():
    raw_data = await fetch(config("URL_V1"))
    ticker_elements = await parse_data(raw_data)
    to_create, to_update = await process_data(ticker_elements)
    if to_create['stocks']:
        task1 = asyncio.create_task(StocksController.create_stocks(to_create))
        await task1
    if to_update['stocks']:
        task2 = asyncio.create_task(
            StocksController.update_stocks(to_update))
        await task2


def scraper():
    asyncio.run(main())
