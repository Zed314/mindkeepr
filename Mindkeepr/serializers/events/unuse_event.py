from rest_framework import serializers
from .event import EventSerializer
from Mindkeepr.models.events import UnUseEvent
from Mindkeepr.models.elements import Element
from Mindkeepr.models import Location

from ..elements.element_short import ElementShortSerializer

@SerializerFactory.register('UnUseEvent')
class UnUseEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    location_destination = LocationShortSerializer()
    location_source = LocationShortSerializer()
    element = ElementShortSerializer()

    class Meta:
        model = UnUseEvent
        fields = EventSerializer.Meta.fields + ("element", "quantity",
                  "location_destination", "location_source")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location_source = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        location_destination = Location.objects.get(
            id=validated_data.pop('location_destination')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        unuse_event = UnUseEvent(**validated_data, element=element,
                                  location_source=location_source, location_destination=location_destination)
        if unuse_event.is_add_to_element_possible():
            unuse_event.save()
            return unuse_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')