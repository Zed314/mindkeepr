from django.db import models
from .element import Element

class Attachment(models.Model):
    name = models.CharField("value", max_length=200, blank=False, null=False, default="")
    file = models.FileField(upload_to="attachments")
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='attachments')
