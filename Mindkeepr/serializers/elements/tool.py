from rest_framework import serializers
from Mindkeepr.models.elements.tool import Tool

from Mindkeepr.serializers.elements.element import ElementFieldMixin
from .element import ElementSerializer



class ToolSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tool
        fields = ElementSerializer.Meta.fields
        depth = 1

    def create(self, validated_data):
        category = self.get_category(validated_data)
        tool = Tool.objects.create(**validated_data,**category)
        return tool