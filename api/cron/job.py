from typing import Callable
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


from config import global_settings

def get_cron_trigger():
    """
    Creates a cron trigger using the global CRONTAB settings.

    :return: A CronTrigger instance configured with the global CRONTAB settings.
    """
    print(global_settings.CRONTAB)
    
    return CronTrigger.from_crontab(global_settings.CRONTAB)

def get_scheduler():
    """
    Creates and returns a new instance of BackgroundScheduler.

    :return: A BackgroundScheduler instance.
    """
    return BackgroundScheduler()

def add_cron_job(fn: Callable):
    """
    Adds a function as a scheduled cron job and starts the scheduler.

    :param fn: The function to be scheduled.
    :return: A BackgroundScheduler instance.
    """
    scheduler = get_scheduler()
    
    scheduler.add_job(fn, get_cron_trigger())

    return scheduler