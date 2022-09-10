import asyncio
from bs4 import BeautifulSoup
from decouple import config
import requests
from scrapper.updater import compare_stock
from scrapper.http_requests import create_stocks, update_clients, update_stocks
import random


def fetch_url(url: str):
    resp = requests.request(method='GET', url=url)
    resp.raise_for_status()
    return resp.text


def parse_data(text_data: str):
    """Converts string data to xml list of elements"""
    soup = BeautifulSoup(text_data, features="xml")
    return soup.select("i")


def process_data(ticker_elements: list):
    update_list = []
    create_list = []
    for element in ticker_elements:
        if element.get('b') == "-":
            continue
        stock = process_ticker(element)
        updated, created = compare_stock(stock)
        if updated:
            asyncio.run(update_clients(updated))
            update_list.append(updated)
        if created:
            asyncio.run(update_clients(created))
            create_list.append(created)
    return [update_list, create_list]


def process_ticker(element):
    """Describe the acronym symbols"""
    stock = {}
    stock['ticker'] = element.get('a')
    price = stock['price'] = float(element.get('b').replace(',', ''))
    change = float(element.get('d')) if element.get('d') != None else 0
    change_direction = element.get('f')
    change = change*-1 if change_direction == 'l' else change
    open_price = stock['open_price'] = round(price - change, 2)
    stock['percentage_change'] = round(
        change*100/open_price, 2)
    return stock


def main():
    raw_data = fetch_url(config("URL_V1"))
    ticker_elements = parse_data(raw_data)
    update_list, create_list = process_data(ticker_elements)
    if create_list:
        asyncio.run(create_stocks(create_list))

    if update_list:
        asyncio.run(update_stocks(update_list))


def random_gen():
    num = round(random.randint(1, 2), 1)
    if num > 0.5:
        return 1
    return 0

