from rest_framework import serializers
from Mindkeepr.models.location import Location
from .fields import RecursiveField

class LocationShortSerializer(serializers.HyperlinkedModelSerializer):
    # Otherwise cannot be seen by other on updates/create
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Location
        fields = ["id", "name"]
        depth = 2

class LocationSerializerShort(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    url = serializers.HyperlinkedIdentityField(view_name="location-detail", lookup_field='pk')
    nb_children = serializers.IntegerField(read_only=True)
    class Meta:
        model = Location
        fields = ("id", "name","url","nb_children")
        depth = 2

from rest_framework import serializers

class LocationFullSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)

    children = RecursiveField(many=True,required=False)
    class Meta:
        model = Location
        fields = ("id", "name","children")

class LocationSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(required=False)
    parent = LocationSerializerShort()
    children = LocationSerializerShort(many=True,required=False)
    class Meta:
        model = Location
        fields = ("id", "name", "description","parent","children")
        depth = 2
