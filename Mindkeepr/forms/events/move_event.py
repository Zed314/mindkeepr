from Mindkeepr.models.elements import Element
from Mindkeepr.models.project import Project
from Mindkeepr.models.location import Location

from django.forms import ModelForm, ModelChoiceField, IntegerField
from ..mixin import DisableFieldsMixin
from ..widget import ProjectWidget, LocationWidget
from Mindkeepr.models.events import MoveEvent


class MoveEventForm(DisableFieldsMixin,ModelForm):
    """ Form for MoveEvent """
    location_source = ModelChoiceField(
        queryset=Location.objects.all())
    element = ModelChoiceField(queryset=Element.objects.all())
    quantity = IntegerField(min_value=1)
    #location_destination = forms.ModelChoiceField(
    #    queryset=models.Location.objects.all())
    project = ModelChoiceField(
        queryset=Project.objects.all(),required=False)
    class Meta:
        model = MoveEvent
        fields = ['comment', 'element', 'quantity','project', 'status',
                  'location_source', 'location_destination']
        widgets = {
            "location_destination": LocationWidget,
            "project" : ProjectWidget
        }

