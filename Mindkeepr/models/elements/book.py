
from .element import Element

class Book(Element):
    """ Book """
    # TODO Add ISBN/Barcode
    def is_unique(self):
        return True
