from rest_framework import serializers
from Mindkeepr.models.elements.movie import MovieCase, Movie, MovieGenre

from .element import ElementFieldMixin, ElementSerializer
from ..serializer_factory import SerializerFactory

@SerializerFactory.register("MovieCase")
class MovieCaseSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):

    category_box_display = serializers.SerializerMethodField(read_only=True, source='get_category_box_display')
    custom_id_display = serializers.SerializerMethodField(read_only=True, source='get_custom_id_display')

    class Meta:
        model = MovieCase
        fields = ["id","custom_id_display","name","format_disk","subformat_disk","nb_disk","custom_id","ean","category_box","category_box_display","borrow_history","quantity_owned","type"] #ElementSerializer.Meta.fields
        depth = 1
    def get_category_box_display(self,obj):
            return obj.get_category_box_display()
    def get_custom_id_display(self,obj):
        return obj.custom_id_display()

class MovieGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MovieGenre
        fields = ["id","name_en","name_fr"]


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    cases = MovieCaseSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        #fields = ["local_title","original_language"]
        fields = ["id","poster","original_title","local_title", "catch_phrase","synopsis","trailer_video_url","genres","cases"]
        depth = 1