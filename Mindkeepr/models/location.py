from polymorphic.models import PolymorphicModel
from django.db import models
from django.contrib.auth.models import User




class Location(models.Model):
    """ Location of an Element. """
    """ Todo : add tags, maybe link to a Element (with a special
    type) ex : Drawer, Table, or other Element that may serve as a Location """
    name = models.CharField("name", max_length=200, blank=False, null=False)
    description = models.CharField(
        "description", max_length=200, blank=True, null=False)
    image = models.ImageField(upload_to='imageslocation', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name="children")
    #tags = TaggableManager()
    @property
    def nb_children(self):
        return len(self.children.all())
    def __str__(self):
        return self.name
