from django.forms import FileField

from Mindkeepr.models.elements import Component
from .element import ElementForm


class ComponentForm(ElementForm):
    datasheet = FileField(required=False)
    class Meta:
        model = Component
        fields = ElementForm.fields + ['datasheet']
        widgets = ElementForm.widgets

