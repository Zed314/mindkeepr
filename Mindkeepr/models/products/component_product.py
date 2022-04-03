
from django.db import models
from .product import Product

class ComponentProduct(Product):
    def __str__(self):
        return self.title
