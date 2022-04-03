from Mindkeepr.models.elements import Element
from Mindkeepr.models.location import Location

from django.forms import ModelForm, ModelChoiceField, IntegerField
from ..mixin import DisableFieldsMixin
from ..widget import LocationWidget, ProjectWidget
from Mindkeepr.models.events import UnUseEvent

class UnUseEventForm(DisableFieldsMixin,ModelForm):
    """ Form for UnUseEvent """
    location_source = ModelChoiceField(
        queryset=Location.objects.all())
    element = ModelChoiceField(queryset=Element.objects.all())
    quantity = IntegerField(min_value=1)

    class Meta:
        model = UnUseEvent
        fields = ['comment', 'element', 'quantity','project',
                  'location_source', 'location_destination']
        widgets = {
            "location_destination": LocationWidget,
            "project" : ProjectWidget
        }