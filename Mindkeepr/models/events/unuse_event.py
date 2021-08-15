from django.db import models

from . import Event


class UnUseEvent(Event):
    """ Switchs to FREE the stock_repartition associated to an Element for a projet that is RESERVED"""
    quantity = models.IntegerField("Quantity", null=False, blank=False)

    location_destination = models.ForeignKey(
        'location', on_delete=models.SET_NULL, related_name='destination_for_unuse_event', null=True)

    location_source = models.ForeignKey(
        'location', related_name='source_for_unuse_event', on_delete=models.SET_NULL, null=True)

    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='unuse_history',
                                null=True)



    def is_add_to_element_possible(self):
        return self.element.is_move_element_possible(self.quantity, "RESERVED", "FREE", self.location_source, self.location_destination, self.project, None)

    def _add_to_element(self):
        return self.element.move_element(self.quantity, "RESERVED", "FREE", self.location_source, self.location_destination, self.project, None)


