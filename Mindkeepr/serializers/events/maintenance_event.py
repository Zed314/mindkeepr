from rest_framework import serializers
from django.contrib.auth.models import User

from Mindkeepr.models.events.maintenance_event import MaintenanceEvent
from Mindkeepr.models.elements.machine import Machine

from ..serializer_factory import SerializerFactory
from .event import EventSerializer, EventFieldMixin
from ..elements.element_short import ElementShortSerializer
from ..user import UserSerializerShort

@SerializerFactory.register('MaintenanceEvent')
class MaintenanceEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):
    element = ElementShortSerializer(required=False)
    assignee = UserSerializerShort(required=False)
    class Meta:
        model = MaintenanceEvent
        fields = EventSerializer.Meta.fields + ("assignee", "is_done","scheduled_date","completion_date","element")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        machine = Machine.objects.get(id=validated_data.pop('element')["id"])
        try:
            assignee = User.objects.get(id=validated_data.pop("assignee")["id"])
        except Exception:
            raise serializers.ValidationError('Missing assignee.')
        maintenance_event = MaintenanceEvent(**validated_data, element=machine, assignee=assignee)
        if maintenance_event.is_add_to_element_possible():
            maintenance_event.save()
            return maintenance_event
        else:
            raise serializers.ValidationError('Event can not be added to element.')

    def update(self, instance, validated_data):

        instance = MaintenanceEvent.objects.get(id=instance.id)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.is_done = validated_data.get('is_done', instance.is_done)
        instance.scheduled_date = validated_data.get('scheduled_date', instance.scheduled_date)
        instance.save()
        return instance