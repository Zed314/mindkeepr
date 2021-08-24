from rest_framework import serializers
from .event import EventSerializer
from Mindkeepr.models.events import BorrowEvent, ReturnEvent
from Mindkeepr.models import Location

from .event import EventFieldMixin
from .borrow_event_short import BorrowEventShortSerializer
from ..elements.element_short import ElementShortSerializer
from ..location import LocationShortSerializer
from ..serializer_factory import SerializerFactory

class ReturnEventSerializerShort(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    location_destination = LocationShortSerializer()

    is_date_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = ReturnEvent
        fields = EventSerializer.Meta.fields + ("is_date_overdue",
                   "location_destination")
        depth = 2
        ordering = EventSerializer.Meta.ordering

@SerializerFactory.register('ReturnEvent')
class ReturnEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    location_destination = LocationShortSerializer()

    borrow_associated = BorrowEventShortSerializer()
    is_date_overdue = serializers.BooleanField(read_only=True)
    element = ElementShortSerializer(read_only=True)
    class Meta:
        model = ReturnEvent
        fields = EventSerializer.Meta.fields + ("element","is_date_overdue",
                   "location_destination","borrow_associated")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location_destination= Location.objects.get(
            id=validated_data.pop('location_destination')["id"])
        borrow_event = BorrowEvent.objects.get(id=validated_data.pop('borrow_associated')["id"])

        return_event = ReturnEvent(**validated_data, borrow_associated=borrow_event,
                    location_destination=location_destination,
                    )
        if return_event.is_add_to_element_possible():
            return_event.save()
            return return_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')