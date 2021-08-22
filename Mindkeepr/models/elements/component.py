
from django.db import models

from . import mixins
from . import Element

class Component(mixins.Consumable,Element):
    """ Electronic component """
    datasheet = models.FileField(upload_to='datasheet', blank=True, null=True)
    pass
