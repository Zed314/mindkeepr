from rest_framework import serializers

from .event import EventSerializer, EventFieldMixin
from Mindkeepr.models.events.move_event import MoveEvent
from Mindkeepr.models.elements.element import Element
from Mindkeepr.models.location import Location
from ..serializer_factory import SerializerFactory
from ..elements.element_short import ElementShortSerializer
from ..location import LocationShortSerializer

@SerializerFactory.register('MoveEvent')
class MoveEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):
    element = ElementShortSerializer()
    location_source = LocationShortSerializer()
    location_destination = LocationShortSerializer()
    class Meta:
        model = MoveEvent
        fields = EventSerializer.Meta.fields + ("element", "quantity",
                  "location_destination", "location_source")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        self.add_event_read_only_default_fields(validated_data)
        location_source = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        location_destination = Location.objects.get(
            id=validated_data.pop('location_destination')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        move_event = MoveEvent(**validated_data, element=element,
                             location_source=location_source, location_destination=location_destination)
        if move_event.is_add_to_element_possible():
            move_event.save()
            return move_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')