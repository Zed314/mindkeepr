from rest_framework import serializers
from Mindkeepr.models.stock_repartition import StockRepartition
from .location import LocationSerializer
from .project import ProjectSerializer
from .elements.element_short import ElementShortSerializer


class StockRepartitionSerializer(serializers.HyperlinkedModelSerializer):

    location = LocationSerializer()
    project = ProjectSerializer()
    element = ElementShortSerializer()
    class Meta:
        model = StockRepartition
        fields = ("id", "quantity", "location", "project","element", "status")
        depth = 2