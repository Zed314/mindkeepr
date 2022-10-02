

import datetime
from Mindkeepr.models import StaffSettings
from django.forms import ValidationError

def retrict_on_open_days(value):

    if StaffSettings.is_open_for_borrow(value):
        if value < datetime.date.today():
            raise ValidationError("The date cannot be in the past !")
        return value
    else:
        raise ValidationError("Sorry, out of opened days for borrow !")
