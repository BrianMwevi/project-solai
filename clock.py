from apscheduler.schedulers import background
# from core.emailer import update_tracker
# from core.models import Watchlist
# from core import crawler_v3, crawler_v4
from scrapper import spider_v1


scheduler = background.BackgroundScheduler()


# def scrap():
#     try:
#         crawler_v1.main()
#     except:
#         print("Erro in jobs")


# def schedule_email():
#     stocks = Watchlist.objects.filter(in_queue=True)
#     if stocks:
#         for stock in stocks:
#             update_tracker(stock)
#     return "No stocks in watchlist"


def start():
    print("Running....")
    # scheduler.add_job(scrap, 'cron', day_of_week='mon-sun', hour='0-23', minute="0-59/1", id='update_stock')
    scheduler.add_job(spider_v1.main, 'interval', seconds=10,
                      id='update_stocks', replace_existing=True)
    # scheduler.add_job(schedule_email, 'interval', seconds=30,replace_existing=True)
    # scheduler.add_job(schedule_email, 'cron', day_of_week='mon-sun',
    #                   hour='0-23', id='send_email', replace_existing=True)
    scheduler.start()
