from apscheduler.schedulers.background import BackgroundScheduler
from newsletter.management.commands import submit_newsletter

sched = BackgroundScheduler()
sched.start()

@sched.scheduled_job(scheduled_job, day_of_week='mon-fri', hour=0-23, minute=0-59, second=10)
def scheduled_job():
    print("Hello, World!")
    return submit_newsletter
