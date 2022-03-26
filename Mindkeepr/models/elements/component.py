
from django.db import models
from itertools import count, filterfalse

from .mixins import Consumable
from .element import Element

class Component(Consumable,Element):
    """ Electronic component """
    datasheet = models.FileField(upload_to='datasheet', blank=True, null=True)

    def refresh_barcode_effective(self):
        self.barcode_effective = self.id_barcode

    def set_custom_id(self):

        if not self.custom_id_generic:
            listid = list(Component.objects.all().values_list('custom_id_generic', flat=True))
            newid = next(filterfalse(set(listid).__contains__, count(1)))
            self.custom_id_generic = newid

    def refresh_custom_id_prefix_generic(self):
        self.custom_id_prefix_generic="X"
