from datetime import datetime
from django.utils import timezone


def today_date():
    today = datetime.today()  # or datetime.now to use local timezone
    day_start = datetime(year=today.year, month=today.month,
                         day=today.day, hour=0, second=0)
    return timezone.make_aware(day_start)
