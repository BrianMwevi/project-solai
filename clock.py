from apscheduler.schedulers import background
from spider.scraper import main
from datetime import datetime

scheduler = background.BackgroundScheduler()


def start():
    scheduler.add_job(main, 'cron',
                      day_of_week='mon-fri', hour='9-20', second='*/5', id="spider")
    scheduler.start()


def market_is_open() -> bool:
    (open_hour, close_hour) = 9, 20
    now = datetime.now()
    next_run = scheduler.get_job("spider").next_run_time

    return next_run.day == now.day and open_hour <= now.hour <= close_hour
