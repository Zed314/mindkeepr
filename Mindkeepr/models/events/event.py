from polymorphic.models import PolymorphicModel
from django.db import models
from django.contrib.auth.models import User


class Event(PolymorphicModel):
    """ Represents an event that occurs on an Element and acts on its stock_repartitions """
    comment = models.CharField(
        "description", max_length=200, blank=True, null=False)
    recording_date = models.DateTimeField(
        "Recording date", auto_now_add=True, blank=False, null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('Project',
                                on_delete=models.SET_NULL,
                                related_name='Events',
                                null=True)
    @property
    def type(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        if not self.id:
            if not self._add_to_element():
                raise ValueError("Event can not be added")
        super().save(*args, **kwargs)