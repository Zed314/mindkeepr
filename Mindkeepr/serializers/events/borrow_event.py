from rest_framework import serializers

from Mindkeepr.models.events import BorrowEvent
from Mindkeepr.models.elements import Element
from Mindkeepr.models import Location
from ..serializer_factory import SerializerFactory
from .event import EventSerializer, EventFieldMixin
from ..location import LocationShortSerializer
from ..elements.element_short import ElementShortSerializer
from .return_event import ReturnEventSerializerShort

@SerializerFactory.register('BorrowEvent')
class BorrowEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    location_source = LocationShortSerializer()
    element = ElementShortSerializer()
    is_returned = serializers.ReadOnlyField()
    return_event = ReturnEventSerializerShort(required=False)
    class Meta:
        model = BorrowEvent
        fields = EventSerializer.Meta.fields + ("element", "quantity", "is_returned",
                  "scheduled_return_date", "location_source","return_event")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location_source = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        borrow_event = BorrowEvent(**validated_data, element=element,
                             location_source=location_source)
        if borrow_event.is_add_to_element_possible():
            borrow_event.save()
            return borrow_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')