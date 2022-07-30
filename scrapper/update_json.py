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

