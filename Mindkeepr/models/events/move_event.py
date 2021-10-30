
from django.db import models
from .event import Event

class MoveEvent(Event):
    """ Change location of a stock_repartition """
    # TODO : Use

    STATUS = {
        ('FREE', "Free"),
        ('RESERVED', "Reserved")
    }

    quantity = models.IntegerField("Quantity", null=False, blank=False)

    location_destination = models.ForeignKey(
        'location', on_delete=models.SET_NULL, related_name='destination_for_move_event', null=True)

    location_source = models.ForeignKey(
        'location', on_delete=models.SET_NULL, related_name='source_for_move_event',  null=True)

    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='move_history',
                                null=True)

    """ Current status """
    status = models.CharField("Status",
                              null=False,
                              blank=False,
                              max_length=200,
                              choices=STATUS)

    def is_add_to_element_possible(self):
        return self.element.is_move_element_possible(self.quantity, self.status, self.status, self.location_source, self.location_destination, self.project, self.project)

    def _add_to_element(self):
        #print(self.location_destination,flush=True)
        return self.element.move_element(self.quantity, self.status, self.status, self.location_source, self.location_destination, self.project, self.project)
