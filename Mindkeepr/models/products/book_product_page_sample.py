from django.db import models
from .book_product import BookProduct

class BookProductPageSample(models.Model):
    name = models.CharField("name", max_length=200, blank=False, null=False, default="")
    image = models.ImageField(upload_to="book_product_page_samples")
    order = models.IntegerField(blank=False,null=False)
    book_product = models.ForeignKey(BookProduct, on_delete=models.CASCADE, related_name='samples')
