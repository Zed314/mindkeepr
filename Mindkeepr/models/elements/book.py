
from .element import Element
from django.db import models
from itertools import count, filterfalse

class Book(Element):
    """ Book """
    isbn = models.CharField(max_length=13,unique=False, null=True)
    ean = models.CharField(max_length=13,unique=False, null=True)
    use_ean_as_effective_barcode = models.BooleanField("Use ean as effective barcode",null=False,default=True,blank=False)
    def is_unique(self):
        return True

    #def custom_id_display(self):
    #    if self.custom_id_generic:
    #        return "{}{:03d}".format("L",self.custom_id_generic)
    #    else:
    #        return self.name


    def __str__(self):
        if self.custom_id_generic:
            return "{} ({}{:03d})".format(self.name,"L",self.custom_id_generic)
        else:
            return self.name

    def refresh_barcode_effective(self):
        if self.use_ean_as_effective_barcode:
            self.barcode_effective = self.ean
        else:
            self.barcode_effective = self.id_barcode

    def refresh_custom_id_prefix_generic(self):
        self.custom_id_prefix_generic="L"

    def set_custom_id(self):

        if not self.custom_id_generic:
            listid = list(Book.objects.all().values_list('custom_id_generic', flat=True))
            print(listid)
            newid = next(filterfalse(set(listid).__contains__, count(1)))
            self.custom_id_generic = newid