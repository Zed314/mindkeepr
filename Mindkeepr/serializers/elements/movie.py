from rest_framework import serializers
from Mindkeepr.models.elements.movie import MovieCase, Movie, MovieGenre

from .element import ElementFieldMixin, ElementSerializer
from ..serializer_factory import SerializerFactory

@SerializerFactory.register("MovieCase")
class MovieCaseSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MovieCase
        fields = ["id","format_disk","subformat_disk","nb_disk","custom_id","ean","category_box","borrow_history"] #ElementSerializer.Meta.fields
        depth = 1

    #def create(self, validated_data):
    #    category = self.get_category(validated_data)
    #    moviecase = MovieCase.objects.create(**validated_data,**category)
    #    return moviecase
class MovieGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MovieGenre
        fields = ["id","name_en","name_fr"]
#@SerializerFactory.register("Movie")
class MovieSerializer(serializers.HyperlinkedModelSerializer):
    cases = MovieCaseSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        #fields = ["local_title","original_language"]
        fields = ["id","poster","original_title","local_title", "catch_phrase","synopsis","trailer_video_url","genres","cases"]
        depth = 1

    #def create(self, validated_data):
    #    #category = self.get_category(validated_data)
    #    movie = Movie.objects.create(**validated_data)
    #    return movie