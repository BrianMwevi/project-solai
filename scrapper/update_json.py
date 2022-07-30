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


def create_stock(stock, stocks):
    """ Create/adds a new stock into the json_stocks.json file.

    :param stock: stock to create
    :type stock: dict
    :return True
    :rtype: bool
    """

    stocks[stock['ticker']] = stock
    stocks_file = os.getcwd() + '/scrapper/json_stocks.json'
    with open(stocks_file, 'w') as fp:
        json.dump(stocks, fp)
        return True


def update_stock(new_stock, stocks):
    """ Updates stock in json_stocks.json file 

    :param new_stock: the most recent scrapped stock
    :type new_stock: dict
    :return: True
    :rtype: bool
    """

    return create_stock(new_stock, stocks)

