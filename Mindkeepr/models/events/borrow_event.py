
from django.db import models
from datetime import date

from .event import Event
from .return_event import ReturnEvent

class BorrowEvent(Event):
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    scheduled_return_date = models.DateField(
        "Scheduled return date", null=False, blank=False)
    location_source = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)
    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='borrow_history',
                                null=True)

    @property
    def is_date_overdue(self):
        if self.is_returned:
            return self.return_event.is_date_overdue
        else:
            return date.today() > self.scheduled_return_date

    @property
    def is_returned(self):
        try:
            self.return_event
            return True
        except ReturnEvent.DoesNotExist:
            return False

    def is_add_to_element_possible(self):
        return self.element.is_move_element_possible(self.quantity, "FREE", "", self.location_source, None, None, None)

    def _add_to_element(self):
        return self.element.move_element(self.quantity, "FREE", "", self.location_source, None, None, None)
