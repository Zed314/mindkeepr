from rest_framework import serializers
from Mindkeepr.models.elements.movie import MovieCase, Movie

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
        moviecase = MovieCase.objects.create(**validated_data,**category)
        return moviecase

#@SerializerFactory.register("Movie")
class MovieSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Movie
        #fields = ["local_title","original_language"]
        fields = "__all__"
        depth = 1

    #def create(self, validated_data):
    #    #category = self.get_category(validated_data)
    #    movie = Movie.objects.create(**validated_data)
    #    return movie