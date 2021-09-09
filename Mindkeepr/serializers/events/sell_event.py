from rest_framework import serializers
from .event import EventSerializer
from Mindkeepr.models.events.sell_event import SellEvent
from Mindkeepr.models.elements.element import Element
from Mindkeepr.models.location import Location

from .event import EventSerializer, EventFieldMixin
from ..elements.element_short import ElementShortSerializer
from ..location import LocationShortSerializer

from ..serializer_factory import SerializerFactory

@SerializerFactory.register('SellEvent')
class SellEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    element = ElementShortSerializer()
    location_source = LocationShortSerializer()

    class Meta:
        model = SellEvent
        fields = EventSerializer.Meta.fields + ("element",
                  "quantity", "price", "location_source")
        depth = 1
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        self.add_event_read_only_default_fields(validated_data)
        location = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        sell_event = SellEvent(
            **validated_data, element=element, location_source=location)
        if sell_event.is_add_to_element_possible():
            sell_event.save()
            return sell_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')