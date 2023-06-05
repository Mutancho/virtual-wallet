import datetime
import asyncio
import requests
from config.config import settings


async def is_within_time_period(start_time, end_time):
    now = datetime.datetime.now().time()
    return start_time <= now <= end_time


async def schedule_task():
    while True:
        # Calculate the time for the next execution
        current_time = datetime.datetime.now().time()
        next_execution_time = datetime.datetime.combine(
            datetime.datetime.now().date() + datetime.timedelta(days=1),
            current_time
        )

        # Calculate the duration until the next execution
        duration = (next_execution_time - datetime.datetime.now()).total_seconds()

        # Sleep until the next execution
        await asyncio.sleep(duration)

        # Execute the task
        requests.post(f'{settings.base_url}/transactions/recurring')


def run_task_scheduler():
    asyncio.run(schedule_task())
