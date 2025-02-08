from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from cron.analysis_job import run_analysis_job
from cron.job import add_cron_job


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the lifespan of the application, setting up and shutting down the cron scheduler.

    This function starts the cron job scheduler when the application starts
    and shuts it down when the application stops.

    :param app: The FastAPI application instance.
    :yield: Yields control back to the FastAPI application lifecycle.
    """
    # batches all the pending analysis's sessions
    # the batches a programmed to happen in a cron expression by a environment variable. 
    scheduler: BackgroundScheduler = add_cron_job(run_analysis_job)
    
    scheduler.start()
    
    yield
    
    scheduler.shutdown()
    