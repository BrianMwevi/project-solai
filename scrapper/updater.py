from itertools import product
from simple_history.utils import update_change_reason
from stocks_v1.models import Stock
import asyncio
from django.shortcuts import get_object_or_404
import requests
from decouple import config

headers = {
    "Content-Type": "application/json",
}


def check_stock(ticker):
    try:
        stock = Stock.objects.get(ticker__iexact=ticker)
        return [True, stock]
    except Stock.DoesNotExist:
        return [False, None]


def update_stocks(stocks):
    for new_stock in stocks:
        exist, old_stock = check_stock(new_stock['ticker'])
        if exist:
            to_update, stock_to_update = process_update(old_stock, new_stock)
            if to_update:

                dev_url = f"{config('DEV_URL')}/stocks/{old_stock.id}/"
                prod_url = f"{config('PROD_URL')}/stocks/{old_stock.id}/"
                requests.request(
                    method='PUT', url=dev_url, data=stock_to_update)
                requests.request(
                    method='PUT', url=prod_url, data=stock_to_update, headers=headers)
                # TODO: update remote db as well
        else:
            prod_url = f"{config('PROD_URL')}/stocks/"
            dev_url = f"{config('DEV_URL')}/stocks/"
            requests.request(
                method='POST', url=dev_url, data=new_stock)
            requests.request(
                method='POST', url=prod_url, data=new_stock, headers=headers)


def process_update(old_stock, new_stock):
    has_changed = compare_change(old_stock, new_stock)
    if not has_changed:
        return [False, None]
    new_stock["prev_price"] = float(old_stock.price)
    price = new_stock['price']
    open_price = new_stock['open_price']
    max_price = float(old_stock.max_price)
    min_price = float(old_stock.min_price)

    if max_price < price and price > open_price:
        new_stock['max_price'] = price
    elif max_price < open_price:
        new_stock['max_price'] = open_price

    if min_price > price and price < open_price:
        new_stock['min_price'] = price
    elif min_price > open_price:
        new_stock['min_price'] = open_price
    return [True, new_stock]


def compare_change(old_stock, new_stock):
    has_changed = float(
        old_stock.percentage_change) != new_stock['percentage_change']
    return has_changed
