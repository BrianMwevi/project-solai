from decouple import config
from aiohttp import ClientSession


async def update_stocks(update_list, create_list):
    api_url = f"{config('DEV_URL')}/stocks/crud/"
    if update_list:
        data = {"stocks": update_list}
        async with ClientSession() as session:
            updated = await fetch_url(api_url, 'PUT', session, data)

<<<<<<< HEAD
def check_stock(ticker):
    try:
        stock = Stock.objects.get(ticker__iexact=ticker)
        print(stock, stock.id)
        return [True, stock]
    except Stock.DoesNotExist:
        return [False, None]


def update_stocks(stocks):
    for new_stock in stocks:

        exist, old_stock = check_stock(new_stock['ticker'])
        if exist:
            # print(f"Old stocks is {old_stock} Id: {old_stock.id}")
            new_stock['id']= old_stock.id
            to_update, stock_to_update = process_update(old_stock, new_stock)
            if to_update:
                dev_url = f"{config('DEV_URL')}/stocks/{old_stock.id}/"
                prod_url = f"{config('PROD_URL')}/stocks/{old_stock.id}/"
                requests.request(
                    method='PUT', url=dev_url, data=stock_to_update)
                updated_stock = requests.request(
                    method='PUT', url=prod_url, data=stock_to_update)
                print(f"\n{updated_stock.text}\n")
                # TODO: update remote db as well\
                # stock_to_update['id'] = old_stock.id
                # return update_change_reason(stock_to_update, "update")
        else:
            print("Creating stocks ... ")
            prod_url = f"{config('PROD_URL')}/stocks/"
            dev_url = f"{config('DEV_URL')}/stocks/"
            requests.request(
                method='POST', url=dev_url, data=new_stock)
            created_stock = requests.request(
                method='POST', url=prod_url, data=new_stock)
            # update_change_reason(created_stock, "Genesis Stock")


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
=======
    if create_list:
        data = {"stocks": create_list}
        async with ClientSession() as session:
            created = await fetch_url(api_url, 'POST', session, data)
    return True


async def fetch_url(url: str, method: str, session: ClientSession, data, **kwargs):
    resp = await session.request(method=method, url=url, json=data, **kwargs)
    resp.raise_for_status()
    stocks = await resp.text()
    return stocks
>>>>>>> develop
