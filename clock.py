from apscheduler.schedulers import background
from spider import spider_v2

scheduler = background.BackgroundScheduler()


def start():
    scheduler.add_job(spider_v2.scraper, 'cron',
                      day_of_week='mon-fri', hour='9-15', second='*/5')
    scheduler.start()
