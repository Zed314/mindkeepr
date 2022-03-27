
from rest_framework import serializers
from ..elements.movie import MovieCaseSerializer
from Mindkeepr.models.products.movie_product import MovieProduct, MovieProductGenre
from .product import ProductSerializer
from ..serializer_factory import SerializerFactory


class MovieProductGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MovieProductGenre
        fields = ["id","name_en","name_fr"]

@SerializerFactory.register("MovieProduct")
class MovieProductSerializer(serializers.HyperlinkedModelSerializer):
    cases = MovieCaseSerializer(many=True, read_only=True)
    genres = MovieProductGenreSerializer(many=True, read_only=True)
    class Meta:
        model = MovieProduct
        #fields = ["title","original_language"]
        fields =  ProductSerializer.Meta.fields + ["id","poster","original_title","title", "catch_phrase","synopsis","trailer_video_url","genres","cases"]
        depth = 1