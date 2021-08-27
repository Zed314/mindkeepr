
from rest_framework import serializers

from Mindkeepr.models.elements import Machine
from .element import ElementSerializer, ElementFieldMixin

from ..events.maintenance_event import MaintenanceEventSerializer
from ..serializer_factory import SerializerFactory

@SerializerFactory.register("Machine")
class MachineSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):

    maintenance_history = MaintenanceEventSerializer(many=True, read_only=True)
    #def get_status_name(self, obj):
     #   return obj.get_status_display()
    #status = serializers.SerializerMethodField(read_only=True, source='get_status_name')
    status= serializers.CharField(
        source='get_status_display',read_only=True
    )
    class Meta:
        model = Machine
        fields = ElementSerializer.Meta.fields + ("maintenance_history","status")
        depth = 1

    def create(self, validated_data):
        category = self.get_category(validated_data)
        machine = Machine.objects.create(**validated_data,**category)
        return machine


