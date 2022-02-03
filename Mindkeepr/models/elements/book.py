
from .element import Element
from django.db import models

class Book(Element):
    """ Book """
    custom_id = models.IntegerField("Custom id", unique=True, null=True, blank=False)
   # ean = models.CharField(max_length=13,unique=True, null=True)
    isbn = models.CharField(max_length=13,unique=True, null=True)
    def is_unique(self):
        return True