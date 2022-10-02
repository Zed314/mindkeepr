from Mindkeepr.models.elements import Machine

from django.forms import ModelForm, ModelChoiceField
from ..mixin import DisableFieldsMixin
from Mindkeepr.models.events import IncidentEvent


class IncidentEventForm(DisableFieldsMixin, ModelForm):
    """ Form for incident event (Machine only) """
    element = ModelChoiceField(queryset=Machine.objects.all())

    class Meta:
        model = IncidentEvent
        fields = ['element', 'new_status', 'comment']