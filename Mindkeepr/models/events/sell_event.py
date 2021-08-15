

from django.db import models

from . import Event

class SellEvent(Event):
    """ Delete and sells the UNRESERVED stock_repartition associated """
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    price = models.FloatField("Price", null=False, blank=False)
    location_source = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)
    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='sell_history',
                                null=True)


    def is_add_to_element_possible(self):
        return self.element.is_move_element_possible(self.quantity, "FREE", "", self.location_source, None, None, self.project)

    def _add_to_element(self):
        return self.element.move_element(self.quantity, "FREE", "", self.location_source, None, None, self.project)
