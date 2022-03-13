from rest_framework import serializers
from Mindkeepr.models.elements.videogame import VideoGame

from Mindkeepr.serializers.elements.element import ElementFieldMixin
from .element import ElementSerializer
from ..serializer_factory import SerializerFactory

@SerializerFactory.register("VideoGame")
class VideoGameSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):
    custom_id_display = serializers.CharField(read_only=True)
    platform_display = serializers.SerializerMethodField(read_only=True, source='get_platform_display')
    class Meta:
        model = VideoGame
        fields = ElementSerializer.Meta.fields + ("custom_id_display","platform","platform_display","barcode_effective")
        depth = 1
    def get_platform_display(self,obj):
            return obj.get_platform_display()

    def create(self, validated_data):
        category = self.get_category(validated_data)
        vg = VideoGame.objects.create(**validated_data, **category)
        return vg