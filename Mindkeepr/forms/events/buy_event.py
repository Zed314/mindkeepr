from Mindkeepr.models.elements import Element
from Mindkeepr.models.project import Project

from django.forms import ModelForm, ModelChoiceField
from ..mixin import DisableFieldsMixin
from ..widget import LocationWidget, ProjectWidget
from Mindkeepr.models.events import BuyEvent

class BuyEventForm(DisableFieldsMixin, ModelForm):
    """ Form that handles creation of buy events """
    #location_destination = forms.ModelChoiceField(
    #    queryset=models.Location.objects.all())
    element = ModelChoiceField(queryset=Element.objects.all())
    project = ModelChoiceField(queryset=Project.objects.all(), required=False)
    class Meta:
        model = BuyEvent
        fields = ['element', 'quantity', 'price', 'supplier',
                  'location_destination','project', 'comment']
        widgets = {
            "location_destination": LocationWidget,
            "project" : ProjectWidget
        }