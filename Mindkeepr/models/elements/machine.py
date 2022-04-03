
from django.db import models

from itertools import count, filterfalse

from Mindkeepr.models.products.machine_product import MachineProduct
from .element import Element



class Machine(Element):
    def is_unique(self):
        return True
    STATUS = [
       ('TRA', "To be disposed"),
       ('INV', "To be tested"),
       ('REP', "To be repared"),
       ('REF', "To be refilled"),
       ('MEH', "Partially working"),
       ('OK', "Working"),
    ]
    status = models.CharField(
        max_length=3,
        choices=STATUS,
        default="OK",
    )

    MACHINE_TYPE = [
       ('HHW', "Hardware"),
       ('GHW', "Gaming Hardware"),
       ('VHW', "Video Hardware"),
       #("UNK", "UNKNOWN")
    ]
    machine_type = models.CharField(
        max_length=3,
        choices=MACHINE_TYPE,
        default="HHW",
        null=False,
        blank=False
    )

    def set_custom_id(self):

        if not self.custom_id_generic:
            listid = list(Machine.objects.filter(machine_type=self.machine_type).values_list('custom_id_generic', flat=True))
            newid = next(filterfalse(set(listid).__contains__, count(1)))
            self.custom_id_generic = newid

    def refresh_custom_id_prefix_generic(self):
        self.custom_id_prefix_generic=self.machine_type[0]



    def refresh_barcode_effective(self):
        self.barcode_effective = self.id_barcode

    @staticmethod
    def product_class():
        return MachineProduct