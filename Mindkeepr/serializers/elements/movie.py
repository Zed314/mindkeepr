from rest_framework import serializers
from Mindkeepr.models.elements.movie import MovieCase, Movie, MovieGenre

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
class MovieGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MovieGenre
        fields = ["id","name_en","name_fr"]
#@SerializerFactory.register("Movie")
class MovieSerializer(serializers.HyperlinkedModelSerializer):
    first_genre = serializers.CharField(source='get_first_genre_display')
    second_genre = serializers.CharField(source='get_second_genre_display')
    class Meta:
        model = Movie
        #fields = ["local_title","original_language"]
        fields = ["id","poster","original_title","local_title", "catch_phrase","synopsis","trailer_video_url","genres","first_genre","second_genre"]
        depth = 1

    #def create(self, validated_data):
    #    #category = self.get_category(validated_data)
    #    movie = Movie.objects.create(**validated_data)
    #    return movie