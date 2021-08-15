
from django.db import models
from .event import Event


class UseEvent(Event):
    """ Switchs to RESERVED the stock_repartition associated to an Element for a projet """
    quantity = models.IntegerField("Quantity", null=False, blank=False)

    location_destination = models.ForeignKey(
        'location', on_delete=models.SET_NULL, related_name='origin_destination_for_use_event', null=True)

    location_source = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)

    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='use_history',
                                null=True)



    def is_add_to_element_possible(self):
        return self.element.is_move_element_possible(self.quantity, "FREE", "RESERVED", self.location_source, self.location_destination, None, self.project)

    def _add_to_element(self):
        return self.element.move_element(self.quantity, "FREE", "RESERVED", self.location_source, self.location_destination, None, self.project)


