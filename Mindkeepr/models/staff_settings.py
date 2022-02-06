from .singleton import SingletonModel
from django.db import models

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

class StaffSettings(SingletonModel):
    support = models.EmailField(default='support@example.com')
    open_day_borrow = models.ManyToManyField(Days)