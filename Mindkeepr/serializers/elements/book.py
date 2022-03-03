from rest_framework import serializers
from Mindkeepr.models.elements.book import Book

from Mindkeepr.serializers.elements.element import ElementFieldMixin
from .element import ElementSerializer
from ..serializer_factory import SerializerFactory

@SerializerFactory.register("Book")
class BookSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):
    custom_id_display = serializers.CharField(read_only=True)
    class Meta:
        model = Book
        fields = ElementSerializer.Meta.fields + ("custom_id_display","barcode_effective")
        depth = 1

    def create(self, validated_data):
        category = self.get_category(validated_data)
        book = Book.objects.create(**validated_data, **category)
        return book