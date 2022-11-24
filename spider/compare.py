import json
import os
from asgiref.sync import async_to_sync
# TODO: Use OOP --> convert all funcs to class methods

# @async_to_sync


class Compare:
    """
    Compares, creates and updates stocks in the json file.
    """
    @classmethod
    def stock_changed(cls, stock):
        """
        Checks if the incoming stock is new or changed and returns a tuple of boolean values (new, changed)
        """
        old_stock = cls.get_stock(stock["ticker"])
        if old_stock is None:
            return True, False
        changed = old_stock['change'] != stock['change']
        return False, changed

    @classmethod
    def create_stock(cls, new_stock):
        open_price = new_stock['open']
        high,  low = cls.get_high_low(new_stock['price'], open_price)
        new_stock['high'] = high
        new_stock['low'] = low
        return cls.save_stock(new_stock)

    @classmethod
    def save_stock(cls, stock):
        """Saves a new stock to json file. Returns None"""
        stocks = cls.get_stocks()
        stocks[stock['ticker']] = stock
        stocks_file = cls.get_json_file()
        with open(stocks_file, 'w') as fp:
            json.dump(stocks, fp)
        return stock

    @classmethod
    def update_stock(cls, new_stock):
        """ Updates stock in stocks.json file. Returns None"""
        old_stock = cls.get_stock(new_stock['ticker'])
        to_update = cls.set_pricing(new_stock, old_stock)
        return cls.save_stock(to_update)

    def get_json_file():
        """
        Creates stocks.json file if missing and returns the file path
        """
        file_path = '/spider/stocks.json'
        if not os.path.exists(os.getcwd() + file_path):
            f = open(os.getcwd() + file_path, "x")
        return os.getcwd() + file_path

    @classmethod
    def get_stock(cls, ticker):
        """
        Gets a stock using the ticker symbol and returns None if not found
        """
        stocks_file = cls.get_json_file()
        with open(stocks_file, 'r') as fp:
            try:
                stocks = json.load(fp)
                return stocks[ticker]
            except (KeyError, json.decoder.JSONDecodeError):
                return None

    @classmethod
    def get_stocks(cls):
        """
        Gets all stocks using and returns empty dict if no stocks exists
        """
        stocks_file = cls.get_json_file()
        with open(stocks_file, 'r') as fp:
            try:
                stocks = json.load(fp)
                return stocks
            except (KeyError, json.decoder.JSONDecodeError):
                return {}

    @classmethod
    def set_pricing(cls, new_stock, old_stock):
        """
        Sets high, low and close prices for a given stock. Returns the updated stock
        """
        high, low = cls.get_high_low(new_stock['price'], new_stock['open'])

        if high > old_stock['high']:
            new_stock['high'] = high
        if low < old_stock['low']:
            old_stock['low'] = low

        old_stock['close'] = old_stock['price']
        old_stock['price'] = new_stock['price']
        old_stock['change'] = new_stock['change']
        return old_stock

    def get_high_low(price, open_price):
        """
        Compares the difference between the current and opening price. Returns a turple (high, low)
        """
        if price > open_price:
            return price, open_price
        return open_price, price
