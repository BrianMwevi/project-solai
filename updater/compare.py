import json
import os
from stocks_v1.models import PriceNotification, Stock, StockTracker
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

# TODO: Use OOP --> convert all funcs to class methods


def compare_stock(new_stock):
    old_stock = get_stock(new_stock['ticker'])
    updated = created = False
    if old_stock is None:
        created = create_stock(new_stock)
    elif old_stock['percentage_change'] != new_stock['percentage_change']:
        updated = update_stock(new_stock)
    return (updated, created)


def create_stock(new_stock):
    open_price = new_stock['open_price']
    max_price,  min_price = get_min_max(new_stock['price'], open_price)
    new_stock['max_price'] = max_price
    new_stock['min_price'] = min_price
    new_stock['prev_price'] = open_price
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
    to_update = set_pricing(new_stock, old_stock)
    saved_stock = save_stock(to_update)

    return saved_stock


def get_json_file():
    file_path = '/updater/stocks.json'
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


# TODO: Modularize this function to Notification class in notificaions.py file
@database_sync_to_async
def track_price(stock):
    ticker = stock['ticker']
    price = float(stock['price'])
    tracker = StockTracker.check_match(ticker, price)

    if tracker:
        tracker = tracker.update_matched()
        content = f"{ticker}'s price matches your quote of {tracker.quote_price}. Price matched at {tracker.matched_date}"
        connected = get_channel_layer()
        instance = PriceNotification(subscriber=tracker, content=content)
        notification = instance.save_notification()
        subscribers = f"{ticker}{tracker.quote_price}"
        async_to_sync(connected.group_send)(subscribers, {
            "type": "client_message", "data": notification.content})
    return tracker
