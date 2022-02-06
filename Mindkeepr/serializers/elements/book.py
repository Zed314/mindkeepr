from rest_framework import serializers
from Mindkeepr.models.elements.book import Book

from Mindkeepr.serializers.elements.element import ElementFieldMixin
from .element import ElementSerializer
from ..serializer_factory import SerializerFactory

@SerializerFactory.register("Book")
class BookSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):
    custom_id_display = serializers.SerializerMethodField(read_only=True, source='get_custom_id_display')
    class Meta:
        model = Book
        fields = ElementSerializer.Meta.fields + ("custom_id_display",)
        depth = 1

    def create(self, validated_data):
        category = self.get_category(validated_data)
        book = Book.objects.create(**validated_data, **category)
        return book
    def get_custom_id_display(self,obj):
        return obj.custom_id_display()