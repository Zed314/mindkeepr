from calendar import weekday
from .singleton import SingletonModel
from django.db import models
import datetime
DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)

class Days(models.Model):
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    def __str__(self):
            return "%s (%s)" % (self.get_day_display(), self.day)

class DayException(models.Model):
    day = models.DateField(null=False,blank=False)
    def __str__(self):
            return "str(self.day)"

import bisect
class StaffSettings(SingletonModel):
    support = models.EmailField(default='support@example.com')
    open_day_borrow = models.ManyToManyField(Days)
    # If open, got priority over close
    exceptionnaly_open_day_borrow = models.ManyToManyField(DayException, blank=True, related_name="open_days")
    exceptionnaly_close_day_borrow = models.ManyToManyField(DayException, blank=True, related_name="close_days")

    def get_list_open_day_borrow(begin_date, end_date):
        settings = StaffSettings.objects.get_or_create(pk=1)[0]
        weekday_open = set( day["day"] for day in settings.open_day_borrow.all().values('day'))
        closed_days = set( day["day"] for day in settings.exceptionnaly_close_day_borrow.filter(day__gte=begin_date).filter(day__lte=end_date).values('day'))
        special_open_days = set( day["day"] for day in settings.exceptionnaly_open_day_borrow.filter(day__gte=begin_date).filter(day__lte=end_date).values("day"))
        days_period = [begin_date + datetime.timedelta(days=i) for i in range((end_date - begin_date).days + 1)]
        list_open_weekday = [d for d in days_period if d.weekday() in weekday_open ]
        list_open_weekday_without_exclusions = [day for day in list_open_weekday if day not in closed_days]
        for day in special_open_days:
            bisect.insort(list_open_weekday_without_exclusions, day)
        return list_open_weekday_without_exclusions

    def is_open_for_borrow(date):
        settings = StaffSettings.objects.get_or_create(pk=1)[0]
        weekday_open = set( day["day"] for day in settings.open_day_borrow.all().values('day'))
        closed_days = set( day["day"] for day in settings.exceptionnaly_close_day_borrow.all().values('day'))
        special_open_days = set( day["day"] for day in settings.exceptionnaly_open_day_borrow.all().values("day"))
        print("openforborrow")
        print(date.weekday())
        print(weekday_open)
        print(closed_days,flush="True")
        if date.weekday() in weekday_open:
            return not date in closed_days
        return date in special_open_days