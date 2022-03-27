from rest_framework import serializers
from ..elements.book import BookSerializer
from Mindkeepr.models.products.book_product import BookProduct
from .product import ProductSerializer
from ..serializer_factory import SerializerFactory
@SerializerFactory.register("BookProduct")
class BookProductSerializer(serializers.HyperlinkedModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = BookProduct
        fields = ProductSerializer.Meta.fields + ["summary", "books", "nb_pages","release_date", "cover", "author", "author_2"]
        depth = 1