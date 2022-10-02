from rest_framework import serializers
from ..elements.book import BookSerializer
from Mindkeepr.models.products.book_product import BookProduct
from .product import ProductSerializer
from ..serializer_factory import SerializerFactory
@SerializerFactory.register("BookProduct")
class BookProductSerializer(serializers.HyperlinkedModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    image_height = serializers.SerializerMethodField()
    def get_image_height(self, obj):
        if obj.image:
            return obj.image.height
        return 0
    image_width = serializers.SerializerMethodField()
    def get_image_width(self, obj):
        if obj.image:
            return obj.image.width
        return 0
    cover_height = serializers.SerializerMethodField()
    def get_cover_height(self, obj):
        if obj.cover:
            return obj.cover.height
        return 0
    cover_width = serializers.SerializerMethodField()
    def get_cover_width(self, obj):
        if obj.cover:
            return obj.cover.width
        return 0

    class Meta:
        model = BookProduct
        fields = ProductSerializer.Meta.fields + ["summary", "image_width", "image_height", "books", "nb_pages","release_date", "cover", "cover_width", "cover_height","author", "author_2","ean","publisher","book_type"]
        depth = 1