from bs4 import BeautifulSoup
from decouple import config
from spider.http_requests import StocksController
from spider.compare import Compare
import requests
from asgiref.sync import async_to_sync


class Spider:

    def fetch(self, url):
        resp = requests.get(url=url)
        resp.raise_for_status()
        return resp

    def parse_data(self, raw_data):
        soup = BeautifulSoup(raw_data.content, features="xml")
        return soup.select("i")

    def process_data(self, ticker_elements):
        to_create = []
        to_update = []
        for element in ticker_elements:
            if element.get('b') == "-":
                continue
            new, updated = self.stock_compare(self.process_ticker(element))
            if new:
                to_create.append(new)
            elif updated:
                to_update.append(updated)
        return ({"stocks": to_create}, {"stocks": to_update})

    def stock_compare(self, stock):
        new, changed = Compare.stock_changed(stock)
        updated_stock = created_stock = None
        if changed:
            updated_stock = Compare.update_stock(stock)
            async_to_sync(StocksController.update_clients)(updated_stock)
        elif new:
            created_stock = Compare.create_stock(stock)
            async_to_sync(StocksController.update_clients)(created_stock)
        return created_stock, updated_stock

    def process_ticker(self, element):
        stock = {}
        stock['ticker'] = element.get('a')
        price = stock['price'] = float(element.get('b').replace(',', ''))
        change = float(element.get('d')) if element.get('d') != None else 0
        change_direction = element.get('f')
        change = change*-1 if change_direction == 'l' else change
        open_price = stock['open'] = round(price - change, 2)
        stock['change'] = round(change*100/open_price, 2)
        return stock


def main():
    spider = Spider()
    raw_data = spider.fetch(config("URL_V1"))
    ticker_elements = spider.parse_data(raw_data)
    to_create, to_update = spider.process_data(ticker_elements)

    from clock import scheduler

    # TODO: Perform async tasks
    if to_create['stocks']:
        scheduler.add_job(async_to_sync(StocksController.create_stocks), args=[
                          to_create], replace_existing=True)
    if to_update['stocks']:
        scheduler.add_job(async_to_sync(StocksController.update_stocks), args=[
                          to_update], replace_existing=True)
