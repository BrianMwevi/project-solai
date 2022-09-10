from apscheduler.schedulers import background
from spider import spider_v2


scheduler = background.BackgroundScheduler()


def start():
    scheduler.add_job(spider_v2.scraper, 'interval', seconds=5,
                      id='update_stocks', replace_existing=True)
    scheduler.start()
