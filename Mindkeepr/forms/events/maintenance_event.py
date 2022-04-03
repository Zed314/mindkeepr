from Mindkeepr.models.elements import Machine

from django.forms import ModelForm, ModelChoiceField, DateField, DateInput
from ..mixin import DisableFieldsMixin
from ..widget import UserWidget
from Mindkeepr.models.events import MaintenanceEvent

class MaintenanceEventForm(DisableFieldsMixin,ModelForm):
    """ Form that handles creation of consume events """
    element = ModelChoiceField(queryset=Machine.objects.all())
    scheduled_date = DateField(widget=DateInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    class Meta:
        model = MaintenanceEvent
        fields = ['element', 'scheduled_date', 'is_done', 'comment', 'assignee']
        widgets = {
            "assignee": UserWidget
        }