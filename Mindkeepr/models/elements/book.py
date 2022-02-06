
from .element import Element
from django.db import models
from itertools import count, filterfalse

class Book(Element):
    """ Book """
    custom_id = models.IntegerField("Custom id", unique=True, null=False, blank=False)
    isbn = models.CharField(max_length=13,unique=True, null=True)
    def is_unique(self):
        return True

    def custom_id_display(self):
        return "{}{:03d}".format("L",self.custom_id)

    def __str__(self):
        return "{} ({}{:03d})".format(self.name,"L",self.custom_id)


    def set_custom_id(book):

        if not book.custom_id:
            listid = list(Book.objects.all().values_list('custom_id', flat=True))
            print(listid)
            newid = next(filterfalse(set(listid).__contains__, count(1)))
            book.custom_id = newid