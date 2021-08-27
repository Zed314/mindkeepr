from rest_framework import serializers
from .event import EventSerializer
from Mindkeepr.models.events.buy_event import BuyEvent
from Mindkeepr.models.elements.element import Element
from Mindkeepr.models.location import Location
from ..serializer_factory import SerializerFactory
from .event import EventFieldMixin
from ..elements.element_short import ElementShortSerializer
from ..location import LocationShortSerializer
from ..project import ProjectShortSerializer

@SerializerFactory.register('BuyEvent')
class BuyEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    element = ElementShortSerializer()
    location_destination = LocationShortSerializer()
    project = ProjectShortSerializer(required=False)

    class Meta:
        model = BuyEvent
        fields = EventSerializer.Meta.fields + ("element",
                  "price", "supplier", "quantity", "location_destination","project")
        depth = 1
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location = Location.objects.get(
            id=validated_data.pop('location_destination')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        buy_event = BuyEvent(
            **validated_data, element=element, location_destination=location)
        if buy_event.is_add_to_element_possible():
            buy_event.save()
            return buy_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')