from rest_framework import serializers
from .event import EventSerializer
from Mindkeepr.models.events import UseEvent
from Mindkeepr.models.elements import Element
from Mindkeepr.models import Location
from Mindkeepr.serializers.location import LocationShortSerializer
from ..serializer_factory import SerializerFactory
from ..elements.element_short import ElementShortSerializer
from .event import EventFieldMixin
from ..project import ProjectShortSerializer

@SerializerFactory.register('UseEvent')
class UseEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    location_destination = LocationShortSerializer()
    location_source = LocationShortSerializer()
    element = ElementShortSerializer()
    project = ProjectShortSerializer()

    class Meta:
        model = UseEvent
        fields = EventSerializer.Meta.fields + ("element", "quantity",
                  "location_destination", "location_source","project")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location_source = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        location_destination = Location.objects.get(
            id=validated_data.pop('location_destination')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        project = Project.objects.get(id=validated_data.pop('project')["id"])
        use_event = UseEvent(**validated_data, element=element, project=project,
                             location_source=location_source, location_destination=location_destination)
        if use_event.is_add_to_element_possible():
            use_event.save()
            return use_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')