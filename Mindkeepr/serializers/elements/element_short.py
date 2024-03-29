from rest_framework import serializers
from Mindkeepr.models.elements.element import Element

class ElementMinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Element
        fields = ("id", "name")

class ElementShortSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    ean = serializers.CharField(required=False)
    custom_id_display = serializers.CharField(read_only=True)
    class Meta:
        model = Element
        fields = ("id", "custom_id_display", "ean","barcode_effective", "type", "name")
        depth = 2
        extra_kwargs = {
            "type": {
                "read_only": False
            }
        }