import json
import os

# TODO: Use OOP --> convert all funcs to class methods


def compare_stock(new_stock):
    old_stock = get_stock(new_stock['ticker'])
    updated = created = False
    if old_stock is None:
        created = create_stock(new_stock)
    elif old_stock['change'] != new_stock['change']:
        updated = update_stock(new_stock)
    return (updated, created)


def create_stock(new_stock):
    open_price = new_stock['open']
    high,  low = get_min_max(new_stock['price'], open_price)
    new_stock['high'] = high
    new_stock['low'] = low
    # new_stock['prev_price'] = open_price
    return save_stock(new_stock)


def save_stock(stock):
    """Saves a new stock to json file"""
    stocks = get_stocks()
    stocks[stock['ticker']] = stock
    stocks_file = get_json_file()
    with open(stocks_file, 'w') as fp:
        json.dump(stocks, fp)
        return stock


def update_stock(new_stock):
    """ Updates stock in stocks.json file """
    old_stock = get_stock(new_stock['ticker'])
    to_update = None
    if old_stock:
        to_update = set_pricing(new_stock, old_stock)
    saved_stock = save_stock(to_update)
    return saved_stock



def get_json_file():
    file_path = '/spider/stocks.json'
    if not os.path.exists(os.getcwd() + file_path):
        f = open(os.getcwd() + file_path, "x")
    return os.getcwd() + file_path


def get_stock(ticker):

    stocks_file = get_json_file()
    with open(stocks_file, 'r') as fp:
        try:
            stocks = json.load(fp)
            return stocks[ticker]
        except Exception as e:
            return None


def get_stocks():

    stocks_file = get_json_file()
    with open(stocks_file, 'r') as fp:
        try:
            stocks = json.load(fp)
            return stocks
        except Exception as e:
            return {}


def set_pricing(new_stock, old_stock=None):
    """Sets the prices of a given stock"""

    price = new_stock['price']
    open_price = new_stock['open']
    high, low = get_min_max(price, open_price)
    # old_stock.update(new_stock)

    if high > old_stock['high']:
        old_stock['high'] = high

    if low < old_stock['low']:
        old_stock['low'] = low

    old_stock['close'] = old_stock['price']
    return old_stock


def get_min_max(price, open_price):
    """Compares the difference between the current and opening price"""

    if price > open_price:
        return [price, open_price]
    return [open_price, price]
