from Mindkeepr.models.elements import Element
from Mindkeepr.models.location import Location

from django.forms import ModelForm, ModelChoiceField, IntegerField
from ..mixin import DisableFieldsMixin, PresetLocationSourceAndQuantityMixin
from Mindkeepr.models.events import SellEvent
from Mindkeepr.models.stock_repartition import StockRepartition


class SellEventForm(DisableFieldsMixin, PresetLocationSourceAndQuantityMixin, ModelForm):
    """ Form for SellEvent """
    location_source = ModelChoiceField(
        queryset=Location.objects.none())
    element = ModelChoiceField(queryset=Element.objects.filter(
        stock_repartitions__in=StockRepartition.objects.filter(status="FREE")).distinct())
    quantity = IntegerField(min_value=1)

    class Meta:
        model = SellEvent
        fields = ['comment', 'element', 'price', 'quantity', 'location_source']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.preset_location_quantity()
