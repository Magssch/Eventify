from apscheduler.schedulers.background import BackgroundScheduler
from newsletter.management.commands import submit_newsletter

sched = BackgroundScheduler()

@sched.scheduled_job('interval', day_of_week='mon-fri', hour=0-23, minute=0-59, second=10)
def scheduled_job():
    print("Hello, World!")
    return submit_newsletter

sched.start()