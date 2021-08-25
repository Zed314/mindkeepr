from rest_framework import serializers
from Mindkeepr.models.elements.tool import Tool

from .element import ElementFieldMixin, ElementSerializer
from ..serializer_factory import SerializerFactory

@SerializerFactory.register("Tool")
class ToolSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tool
        fields = ElementSerializer.Meta.fields
        depth = 1

    def create(self, validated_data):
        category = self.get_category(validated_data)
        tool = Tool.objects.create(**validated_data,**category)
        return tool