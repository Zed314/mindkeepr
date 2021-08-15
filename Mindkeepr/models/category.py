from polymorphic.models import PolymorphicModel
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """ Category of an Element. Have children and parents. """
    name = models.CharField("name", max_length=40, blank=False, null=False)
    parent = models.ForeignKey(
        "Category", on_delete=models.PROTECT, null=True, blank=True, related_name="children")
    @property
    def nb_children(self):
        return len(self.children.all())
    def __str__(self):
        return self.name