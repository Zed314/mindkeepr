
from .element import Element
from django.db import models
from itertools import count, filterfalse



class BookAbstract(models.Model):
    """ Class that represent a book, but not as the object, rather the concept. """

    title = models.CharField(max_length=100,  null=True, blank=True)

    summary = models.CharField(max_length=2300, blank=True, null=True)
    nb_pages = models.IntegerField(null=True, blank=True)

    release_date = models.DateField( null=True, blank=True)
    cover = models.ImageField(upload_to='book_images/cover', null=True, blank=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    author_2 = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    """ EAN13 """
    ean = models.CharField(max_length=13,unique=False, null=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Undefined title"


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

    book_abstract = models.ForeignKey('BookAbstract',
                                on_delete=models.SET_NULL,
                                related_name='books',
                                null=True)
    #def custom_id_display(self):
    #    if self.custom_id_generic:
    #        return "{}{:03d}".format("L",self.custom_id_generic)
    #    else:
    #        return self.name


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