import json
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

    old_stock, stocks = get_stocks(new_stock)
    if old_stock is None:
        created = create_stock(new_stock, stocks)
        return [False, created]
    if old_stock['percentage_change'] == new_stock['percentage_change']:
        return [False, False]

    updated = update_stock(new_stock, stocks)
    return [updated, False]


def create_stock(new_stock, stocks):
    """ Create/adds a new stock into the stocks.json file.

    :param stock: stock to create
    :type stock: dict
    :return True
    :rtype: bool
    """
    old_stock = new_stock
    old_stock['max_price'] = 0
    old_stock['min_price'] = 0
    stock = get_max_min_price(new_stock, old_stock)
    stocks[new_stock['ticker']] = stock
    stocks_file = os.getcwd() + '/scrapper/stocks.json'
    with open(stocks_file, 'w') as fp:
        json.dump(stocks, fp)
        return True


def update_stock(new_stock, stocks):
    """ Updates stock in stocks.json file 

    :param new_stock: the most recent scrapped stock
    :type new_stock: dict
    :return: True
    :rtype: bool
    """
    old_stock = stocks[new_stock['ticker']]
    new_stock = get_max_min_price(new_stock, old_stock)
    return create_stock(new_stock, stocks)


def get_stocks(new_stock):
    """ Gets specific stock and all available stocks from stocks.json file

    :param new_stock: the most recent scrapped stock
    :type new_stock: dict
    :return specific stock and all available stocks
    :rtype: dict|NoneType
    """

    stocks_file = os.getcwd() + '/scrapper/stocks.json'
    with open(stocks_file, 'r') as fp:
        stocks = {}
        try:
            stocks = json.load(fp)
            stock = stocks[new_stock['ticker']]
            return [stock, stocks]
        except Exception as e:
            return [None, stocks]

# TODO: add function docstring


def get_max_min_price(new_stock, old_stock):
    price = new_stock['price']
    open_price = new_stock['open_price']

    max_price = old_stock['max_price']
    min_price = old_stock['min_price']

    if max_price < price and price > open_price:
        new_stock['max_price'] = price
    elif max_price < open_price:
        new_stock['max_price'] = open_price

    if min_price > price and price < open_price:
        new_stock['min_price'] = price
    elif min_price > open_price:
        new_stock['min_price'] = open_price
    return new_stock
