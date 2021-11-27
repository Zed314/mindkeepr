
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db import models
from django.contrib.auth.models import User

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

    beneficiary = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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
        quantity = 1
        if not self.element.is_unique:
            quantity = self.quantity
            return self.element.is_move_element_possible(quantity, "FREE", "", self.location_source, None, None, None)
        else:
            is_free_of_potential_borrow = not PotentialBorrowEvent.objects.filter(element=self.element).filter(scheduled_return_date__gt=date.today(), scheduled_borrow_date__lt=self.scheduled_return_date).exists()
            return is_free_of_potential_borrow and self.element.is_move_element_possible(quantity, "FREE", "", self.location_source, None, None, None)



    def _add_to_element(self):
        if self.element.is_unique and not self.quantity:
            self.quantity = 1
        if self.is_add_to_element_possible():
            return self.element.move_element(self.quantity, "FREE", "", self.location_source, None, None, None)
        return False

class PotentialBorrowEvent(Event):
    """ Future borrow """
    beneficiary = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    scheduled_borrow_date = models.DateField(
        "Scheduled borrow date", null=False, blank=False)
    scheduled_return_date = models.DateField(
        "Scheduled return date", null=False, blank=False)
    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='future_borrows',
                                null=True)

    @property
    def is_begin_date_overdue(self):
        return  self.scheduled_borrow_date < date.today()

    def is_add_to_element_possible(self):
        if self.element.is_unique and not self.is_begin_date_overdue:
            if self.scheduled_borrow_date < self.scheduled_return_date:
                is_free_of_potential_borrow = not PotentialBorrowEvent.objects.filter(element=self.element).filter(scheduled_return_date__gt=self.scheduled_borrow_date, scheduled_borrow_date__lt=self.scheduled_return_date).exists()
                is_free_of_borrow = not BorrowEvent.objects.filter(element=self.element).filter(scheduled_return_date__gt=self.scheduled_borrow_date, recording_date__lt=self.scheduled_return_date).exists()
                return is_free_of_borrow and is_free_of_potential_borrow
            else:
                return False
        return False

    def _add_to_element(self):
        #for now, only unique is possible, todo :check dates
        return self.is_add_to_element_possible()
