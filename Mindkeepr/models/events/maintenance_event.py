
from django.db import models
from django.contrib.auth.models import User
from . import Event
from ..elements.machine import Machine
from datetime import date

class MaintenanceEvent(Event):
    is_done = models.BooleanField("Is completed ?", null=False, blank=False)
    scheduled_date = models.DateField(
        "Scheduled execution date", null=True, blank=True)
    completion_date = models.DateField(
        "Execution date", null=True, blank=True)
    # Attention ! Is only a machine
    element = models.ForeignKey('Machine',
                                on_delete=models.CASCADE,
                                related_name='maintenance_history',
                                null=True)
    assignee = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    def is_add_to_element_possible(self):
        return True
    def _add_to_element(self):
        if not self.is_done:
            self.completion_date = None
        else :
            self.completion_date = date.today()
        return True

    def save(self, *args, **kwargs):
        self._add_to_element()
        super().save(*args, **kwargs)
