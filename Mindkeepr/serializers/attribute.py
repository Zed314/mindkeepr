from rest_framework import serializers
from Mindkeepr.models import Attribute


class AttributeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Attribute
        fields = ("id", "name", "value")
        depth = 2
