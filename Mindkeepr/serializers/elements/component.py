from rest_framework import serializers

from Mindkeepr.models import Component

from .element import ElementFieldMixin, ElementSerializer
from ..attribute import AttributeSerializer

class ComponentSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):
    attributes = AttributeSerializer(many=True, required=False)

    class Meta:
        model = Component
        fields = ElementSerializer.Meta.fields + ('attributes',"datasheet")
        depth = 1

    def create(self, validated_data):
        category = self.get_category(validated_data)
        component = Component.objects.create(
            **validated_data, **category)#, category=category)
        return component