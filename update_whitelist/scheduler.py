"""
Author: abe<wechat:abrahamgreyson>
Date: 2024/6/13 13:45:18
"""
import schedule
import time


def schedule_jobs(update_frequency):
    schedule.every(update_frequency).seconds.do(update_all)
    while True:
        schedule.run_pending()
        time.sleep(1)
