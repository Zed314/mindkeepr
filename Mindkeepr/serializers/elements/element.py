from rest_framework import serializers

from Mindkeepr.models.elements.element import Element
from Mindkeepr.models.category import Category
from ..category import CategorySerializerShortShort
from ..stock_repartition import StockRepartitionSerializer
from ..events.borrow_event import BorrowEventSerializer
from ..events.buy_event import BuyEventSerializer
from ..events.sell_event import SellEventSerializer
from ..serializer_factory import SerializerFactory

class ElementFieldMixin(serializers.Serializer):
    category = CategorySerializerShortShort()
   # stock_repartitions = StockRepartitionSerializer(many=True, read_only=True)
   # buy_history = BuyEventSerializer(many=True, read_only=True)
   # sell_history = SellEventSerializer(many=True, read_only=True)
   # borrow_history = BorrowEventSerializer(many=True, read_only=True)
   # def get_category(self, validated_data):
   #     try:
   #         category = Category.objects.get(id=validated_data.pop("category")["id"])
   #     except Exception:
   #         raise serializers.ValidationError('Missing category.')
   #     return {"category":category}


class ElementSerializer(serializers.HyperlinkedModelSerializer, SerializerFactory):

    class Meta:
        model = Element
        fields = ("id", "name", "description", "id_barcode", "comment", "category", "quantity_owned","quantity_available",
                  "type", "image")#,"buy_history", "sell_history", "borrow_history")
        depth = 2
        extra_kwargs = {
            "type": {
                "read_only": False
            }
        }

    def to_representation(self, obj):
        """
        Because Event is Polymorphic
        """
        type = obj.__class__.__name__
        serializer = SerializerFactory.create_serializer(type, context=self.context)
        if(serializer):
            return serializer.to_representation(obj)
        # Should not occur
        return super(ElementSerializer, self).to_representation(obj)

    def to_internal_value(self, data):
        """
        Because Event is Polymorphic
        """
        type = data.get('type')
        serializer = SerializerFactory.create_serializer(type,context=self.context)
        if(serializer):
            return serializer.to_internal_value(data)
        return super(ElementSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        type = self.context['request'].data.get('type')
        serializer = SerializerFactory.create_serializer(type,context=self.context)
        if(serializer):
            return serializer.create(validated_data)
        raise serializers.ValidationError('Unknown or missing type.')

    def update(self, instance, validated_data):
        type = self.context['request'].data.get('type')
        serializer = SerializerFactory.create_serializer(type,context=self.context)
        if(serializer):
            return serializer.update(instance,validated_data)
        raise serializers.ValidationError('Unknown or missing type.')