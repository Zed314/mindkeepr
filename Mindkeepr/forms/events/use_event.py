from Mindkeepr.models.elements import Element
from Mindkeepr.models.location import Location

from django.forms import ModelForm, ModelChoiceField, IntegerField
from ..mixin import DisableFieldsMixin, PresetLocationSourceAndQuantityMixin
from ..widget import LocationWidget, ProjectWidget
from Mindkeepr.models.events import UseEvent
from Mindkeepr.models.stock_repartition import StockRepartition


class UseEventForm(DisableFieldsMixin, PresetLocationSourceAndQuantityMixin, ModelForm):
    """ Form for UseEvent """
    location_source = ModelChoiceField(
        queryset=Location.objects.all())
    element = ModelChoiceField(queryset=Element.objects.filter(
        stock_repartitions__in=StockRepartition.objects.filter(status="FREE")).distinct())
    quantity = IntegerField(min_value=1)


    class Meta:
        model = UseEvent
        fields = ['comment', 'element', 'quantity','project',
                  'location_source', 'location_destination']
        widgets = {
            "location_destination": LocationWidget,
            "project" : ProjectWidget
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.preset_location_quantity()
