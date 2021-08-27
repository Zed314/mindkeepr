
from django.db import models

from .event import Event
from ..elements.machine import Machine

class IncidentEvent(Event):
    element = models.ForeignKey('Machine',
                                on_delete=models.CASCADE,
                                related_name='incident_history',
                                null=True)
    #incident_comment = models.CharField("Incident comment", max_length=100, blank=True, null=True)
    new_status = models.CharField(
        max_length=3,
        choices=Machine.STATUS,
        default="INV",
    )
    def is_add_to_element_possible(self):
        return True
    def _add_to_element(self):
        self.element.status=self.new_status
        self.element.save()
        return True
