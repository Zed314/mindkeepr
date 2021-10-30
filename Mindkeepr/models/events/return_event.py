from django.db import models

from .event import Event


class ReturnEvent(Event):

    location_destination = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)
    # Todo : cascade ?
    borrow_associated = models.OneToOneField(
        'BorrowEvent', on_delete=models.CASCADE, null=False, related_name='return_event')

    @property
    def element(self):
        return self.borrow_associated.element

    @property
    def is_date_overdue(self):
        return self.recording_date.date() > self.borrow_associated.scheduled_return_date

    def is_add_to_element_possible(self):
        return self.borrow_associated.element.is_move_element_possible(self.borrow_associated.quantity, "", "FREE", None, self.location_destination, None, None,already_owned=True)

    def _add_to_element(self):
        return self.borrow_associated.element.move_element(self.borrow_associated.quantity, "", "FREE", None, self.location_destination, None, None,already_owned=True)

