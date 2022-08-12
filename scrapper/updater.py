import json
from multiprocessing.spawn import old_main_modules
import os


def compare_stock(new_stock):
    """ Checks if stock has changed or not

    :param new_stock: most recent scrapped stock to compare with old stock
    :type new_stock: dict
    :return True if stock has been updated, False otherwise
    :rtype: array of bool
    :return True if stock has been created, False otherwise
    :rtype: array of bool
    """

    old_stock = get_stock(new_stock['ticker'])
    if old_stock is None:
        created = create_stock(new_stock)
        return (False, created)
    if old_stock['percentage_change'] == new_stock['percentage_change']:
        return (False, False)
    updated = update_stock(new_stock)
    return (updated, False)


def create_stock(new_stock):
    """ Create/adds a new stock into the stocks.json file.

    :param stock: stock to create
    :type stock: dict
    :return True
    :rtype: bool
    """
    price = new_stock['price']
    open_price = new_stock['open_price']
    max_price,  min_price = get_min_max(price, open_price)
    new_stock['max_price'] = max_price
    new_stock['min_price'] = min_price
    new_stock['prev_price'] = open_price
    return save_stock(new_stock)


def save_stock(stock):
    """Saves a new stock to json file"""
    stocks = get_stocks()
    stocks[stock['ticker']] = stock
    stocks_file = os.getcwd() + '/scrapper/stocks.json'
    with open(stocks_file, 'w') as fp:
        json.dump(stocks, fp)
        return stock


def update_stock(new_stock):
    """ Updates stock in stocks.json file 

    :param new_stock: the most recent scrapped stock
    :type new_stock: dict
    :return: True
    :rtype: bool
    """

    old_stock = get_stock(new_stock['ticker'])
    to_update = set_pricing(new_stock, old_stock)
    return save_stock(to_update)


def get_stock(ticker):

    stocks_file = os.getcwd() + '/scrapper/stocks.json'
    with open(stocks_file, 'r') as fp:
        try:
            stocks = json.load(fp)
            return stocks[ticker]
        except Exception as e:
            return None


def get_stocks():

    stocks_file = os.getcwd() + '/scrapper/stocks.json'
    with open(stocks_file, 'r') as fp:
        try:
            stocks = json.load(fp)
            return stocks
        except Exception as e:
            return {}


def set_pricing(new_stock, old_stock=None):
    """Sets the prices of a given stock"""

    price = new_stock['price']
    open_price = new_stock['open_price']
    max_price, min_price = get_min_max(price, open_price)
    old_stock.update(new_stock)

    if max_price > old_stock['max_price']:
        old_stock['max_price'] = max_price

    if min_price < old_stock['min_price']:
        old_stock['min_price'] = min_price

    old_stock['prev_price'] = old_stock['price']
    return old_stock


def get_min_max(price, open_price):
    """Compares the difference between the current and opening price"""

    if price > open_price:
        return [price, open_price]
    return [open_price, price]
