
from rest_framework import serializers
from Mindkeepr.models.elements.movie import MovieCase

from .element import ElementFieldMixin, ElementSerializer
from ..serializer_factory import SerializerFactory

@SerializerFactory.register("MovieCase")
class MovieCaseSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):

    category_box_display = serializers.SerializerMethodField(read_only=True, source='get_category_box_display')
    custom_id_display = serializers.CharField(read_only=True)
    class Meta:
        model = MovieCase
        fields = ["id","custom_id_display","name","id_barcode","format_disk","subformat_disk","nb_disk","custom_id_generic","ean", "barcode_effective", "category_box","category_box_display","quantity_owned","quantity_available","is_new","type"] #ElementSerializer.Meta.fields
        depth = 1
    def get_category_box_display(self,obj):
            return obj.get_category_box_display()