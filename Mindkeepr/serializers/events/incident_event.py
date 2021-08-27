from rest_framework import serializers


from Mindkeepr.models.events.incident_event import IncidentEvent
from Mindkeepr.models.elements.machine import Machine
from ..serializer_factory import SerializerFactory
from .event import EventSerializer, EventFieldMixin
from ..elements.element_short import ElementShortSerializer

@SerializerFactory.register('IncidentEvent')
class IncidentEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):
    element = ElementShortSerializer()
    class Meta:
        model = IncidentEvent
        fields = EventSerializer.Meta.fields + ("element","new_status","get_new_status_display")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        element = Machine.objects.get(id=validated_data.pop('element')["id"])
        incident_event = IncidentEvent(**validated_data, element=element)
        if incident_event.is_add_to_element_possible():
            incident_event.save()
            return incident_event
        else:
            raise serializers.ValidationError('Event can not be added to element.')
