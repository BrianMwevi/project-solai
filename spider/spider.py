from bs4 import BeautifulSoup
from decouple import config
from clock import scheduler
import requests


def fetch(url: str):
    resp = requests.get(url=url)
    resp.raise_for_status()
    xml_data = resp.text
    return xml_data


def parse_data(raw_data):
    soup = BeautifulSoup(raw_data, features="xml")
    return soup.select("i")


def process_data(ticker_elements: list):
    to_create = []
    to_update = []
    for element in ticker_elements:
        if element.get('b') == "-":
            continue
        stock = process_ticker(element)
        (updated, created) = compare_stock(stock)
        if created:
            StocksController.update_clients(created)
            to_create.append(created)
        if updated:
            track_price(updated)
            StocksController.update_clients(updated)
            to_update.append(updated)

    return ({"stocks": to_create}, {"stocks": to_update})


def process_ticker(element):
    stock = {}
    stock['ticker'] = element.get('a')
    price = stock['price'] = float(element.get('b').replace(',', ''))
    change = float(element.get('d')) if element.get('d') != None else 0
    change_direction = element.get('f')
    change = change*-1 if change_direction == 'l' else change
    open_price = stock['open_price'] = round(price - change, 2)
    stock['percentage_change'] = round(change*100/open_price, 2)
    return stock


def scraper():
    raw_data = fetch(config("URL_V1"))
    ticker_elements = parse_data(raw_data)
    to_create, to_update = process_data(ticker_elements)
    if to_create['stocks']:
        scheduler.add_job(StocksController.create_stocks, args=[to_create])
    if to_update['stocks']:
        scheduler.add_job(StocksController.update_stocks, args=[to_update])