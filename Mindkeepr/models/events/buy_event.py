
from django.db import models

from .event import Event
class BuyEvent(Event):
    """ Adds new element with FREE status """
    price = models.FloatField("Price", null=False, blank=False)
    supplier = models.CharField(
        "supplier", max_length=50, blank=True, null=True)
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    location_destination = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)
    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='buy_history',
                                null=True)

    def is_add_to_element_possible(self):
        #if not self.location_destination:
        #    self.location_destination = self.element.default_location
        if self.project:
            return self.element.is_move_element_possible(self.quantity, "", "RESERVED", None, self.location_destination, None, self.project)
        else:
            return self.element.is_move_element_possible(self.quantity, "", "FREE", None, self.location_destination, None, None)

    def _add_to_element(self):
        #if not self.location_destination:
        #    self.location_destination = self.element.default_location
        if self.project:
            return self.element.move_element(self.quantity, "", "RESERVED", None, self.location_destination, None, self.project)
        else :
            return self.element.move_element(self.quantity, "", "FREE", None, self.location_destination, None, None)
