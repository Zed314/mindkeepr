
from . import element

class Book(element.Element):
    """ Book """
    # TODO Add ISBN/Barcode
    def is_unique(self):
        return True
