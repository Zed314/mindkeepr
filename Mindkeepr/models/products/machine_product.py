
from .product import Product

class MachineProduct(Product):
    """ Video game """
    def __str__(self):
        return self.title
