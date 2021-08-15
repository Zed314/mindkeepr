
from django.db import models

from . import Event


class ConsumeEvent(Event):
    """ Deletes the stock_repartition associated for a project """
    """ TODO add project """
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    location_source = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)
    # todo add project
    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='consume_history',
                                null=True)


    def is_add_to_element_possible(self):
        if not self.element.is_consummable:
            return False
        if not self.element.is_move_element_possible(self.quantity, "RESERVED", "", self.location_source, None, self.project, None):
            return self.element.is_move_element_possible(self.quantity, "FREE", "", self.location_source, None, None, None)
        return True

    def _add_to_element(self):
        if not self.element.is_consummable:
            return False
        if not self.element.move_element(self.quantity, "RESERVED", "", self.location_source, None, self.project, None):
            return self.element.move_element(self.quantity, "FREE", "", self.location_source, None, None, None)
        return True