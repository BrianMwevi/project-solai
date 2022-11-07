from apscheduler.schedulers import background
from spider.scraper import scraper

scheduler = background.BackgroundScheduler()


def start():
    scheduler.add_job(scraper, 'cron',
                      day_of_week='mon-fri', hour='9-15', second='*/5')
    scheduler.start()
