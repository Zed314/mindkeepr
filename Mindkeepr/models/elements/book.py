
from Mindkeepr.models.products.book_product import BookProduct
from .element import Element
from django.db import models
from itertools import count, filterfalse




class Book(Element):
    """ Book """
    #isbn = models.CharField(max_length=13,unique=False, null=True)
    ean = models.CharField(max_length=13,unique=False, null=True)
    use_ean_as_effective_barcode = models.BooleanField("Use ean as effective barcode",null=False,default=True,blank=False)
    FORMAT = [
       ('NOV', "Novel"),
       ('COM', "Comic Book"),
       #("UNK", "UNKNOWN")
    ]
    format_book = models.CharField(
        max_length=3,
        choices=FORMAT,
        default="NOV",
    )

    def is_unique(self):
        return True

    @staticmethod
    def product_class():
        return BookProduct


    def __str__(self):
        if self.name and self.custom_id_prefix_generic and self.custom_id_generic:
            return "{} ({}{:03d})".format(self.name,self.custom_id_prefix_generic,self.custom_id_generic)
        else:
            return "None"


    def refresh_barcode_effective(self):
        if self.use_ean_as_effective_barcode:
            if Element.objects.filter(barcode_effective=self.ean).exclude(id=self.id).exists():
                # Already taken.
                self.use_ean_as_effective_barcode = False
                self.barcode_effective = self.id_barcode
            else:
                self.barcode_effective = self.ean
        else:
            self.barcode_effective = self.id_barcode

    def refresh_custom_id_prefix_generic(self):
        self.custom_id_prefix_generic=self.format_book[0]

    def set_custom_id(self):

        if not self.custom_id_generic:
            listid = list(Book.objects.filter(format_book=self.format_book).values_list('custom_id_generic', flat=True))
            newid = next(filterfalse(set(listid).__contains__, count(1)))
            self.custom_id_generic = newid