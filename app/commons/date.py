from django.utils.timezone import datetime, timedelta
from app.settings import env


def get_lunch_time():
    return env.time("LUNCH_START", default="12:00:00")


def get_current_vote_date():
    today = datetime.now()
    lunch_started = today.time() >= get_lunch_time()
    if lunch_started:
        today += timedelta(days=1)
    return today.date()
