from rest_framework import serializers
from Mindkeepr.models.elements.movie import MovieCase

from .element import ElementFieldMixin, ElementSerializer
from ..serializer_factory import SerializerFactory

@SerializerFactory.register("MovieCase")
class MovieCaseSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MovieCase
        fields = ElementSerializer.Meta.fields
        depth = 1

    def create(self, validated_data):
        category = self.get_category(validated_data)
        tool = MovieCase.objects.create(**validated_data,**category)
        return tool