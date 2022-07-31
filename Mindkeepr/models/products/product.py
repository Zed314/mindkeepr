
from polymorphic.models import PolymorphicModel
from django.db import models

class Product(PolymorphicModel):
    title = models.CharField("name", max_length=150, blank=False, null=False)
    image = models.ImageField(upload_to='element_images', blank=True, null=True)
    short_description = models.CharField("description", max_length=150, blank=True, null=False)
    is_new = models.BooleanField("Is new ?",default=False,null=True, blank=False)
    @property
    def type(self):
        return self.__class__.__name__