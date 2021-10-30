
from django.db import models

from .mixins import Consumable
from .element import Element

class Component(Consumable,Element):
    """ Electronic component """
    datasheet = models.FileField(upload_to='datasheet', blank=True, null=True)
    pass
