from rest_framework import serializers
from Mindkeepr.models.elements.element import Element

class ElementMinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Element
        fields = ("id", "name")

class ElementShortSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    custom_id_display = serializers.SerializerMethodField(read_only=True, source='get_custom_id_display')
    class Meta:
        model = Element
        fields = ("id", "custom_id_display", "type", "name")
        depth = 2
        extra_kwargs = {
            "type": {
                "read_only": False
            }
        }
    def get_custom_id_display(self,obj):
        return obj.custom_id_display()