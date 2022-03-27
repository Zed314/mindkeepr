from django.db import models
from .product import Product

class BookProduct(Product):
    """ Class that represent a book, but not as the object, rather the concept. """

    #title = models.CharField(max_length=100,  null=True, blank=True)

    summary = models.CharField(max_length=2300, blank=True, null=True)
    nb_pages = models.IntegerField(null=True, blank=True)
    release_date = models.DateField( null=True, blank=True)
    cover = models.ImageField(upload_to='book_images/cover', null=True, blank=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    author_2 = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)

    """ EAN13 """
    ean = models.CharField(max_length=13,unique=False, null=True)

    BOOK_TYPE = [
       ('CMB', "Comic Book"),
       ('NOV', "Novel"),
    ]


    book_type = models.CharField(
        max_length=3,
        choices=BOOK_TYPE,
        default="CMB",
        null=False,
        blank=False
    )

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Undefined title"