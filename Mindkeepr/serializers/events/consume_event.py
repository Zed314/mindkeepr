from rest_framework import serializers
from .event import EventSerializer
from Mindkeepr.models.events.consume_event import ConsumeEvent
from Mindkeepr.models.elements import Element
from Mindkeepr.models.location import Location

from ..location import LocationShortSerializer
from ..elements.element_short import ElementShortSerializer
from .event import EventFieldMixin
from ..serializer_factory import SerializerFactory

@SerializerFactory.register('ConsumeEvent')
class ConsumeEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):
    location_source = LocationShortSerializer()
    element = ElementShortSerializer()
    class Meta:
        model = ConsumeEvent
        fields = EventSerializer.Meta.fields + (
                  "quantity", "element", "location_source")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        self.add_event_read_only_default_fields(validated_data)
        location_source = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        event = ConsumeEvent(**validated_data, element=element, location_source=location_source)
        if event.is_add_to_element_possible():
            event.save()
            return event
        else:
            raise serializers.ValidationError('Event can not be added to element.')
