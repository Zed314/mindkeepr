from Mindkeepr.models.elements import *
from Mindkeepr.models.category import Category
from ..category import CategorySerializerShortShort
from ..stock_repartition import StockRepartitionSerializer
from ..events.borrow_event import BorrowEventSerializer
from ..events.buy_event import BuyEventSerializer
from ..events.sell_event import SellEventSerializer
from rest_framework import serializers


class ElementFieldMixin(serializers.Serializer):
    category = CategorySerializerShortShort()
    stock_repartitions = StockRepartitionSerializer(many=True, read_only=True)
    buy_history = BuyEventSerializer(many=True, read_only=True)
    sell_history = SellEventSerializer(many=True, read_only=True)
    borrow_history = BorrowEventSerializer(many=True, read_only=True)
    def get_category(self, validated_data):
        try:
            category = Category.objects.get(id=validated_data.pop("category")["id"])
        except Exception:
            raise serializers.ValidationError('Missing category.')
        return {"category":category}


class ElementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Element
        fields = ("id", "name", "description", "comment", "category", "quantity_owned",
                  "type", "stock_repartitions", "image","buy_history", "sell_history", "borrow_history")
        depth = 2
        extra_kwargs = {
            "type": {
                "read_only": False
            }
        }

    def to_representation(self, obj):
        """
        Because Element is Polymorphic
        """
        if isinstance(obj, Component):
            return ComponentSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, Machine):
            return MachineSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, Tool):
            return ToolSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, Book):
            return BookSerializer(obj, context=self.context).to_representation(obj)
        return super(ElementSerializer, self).to_representation(obj)

    def to_internal_value(self, data):
        """
        Because Element is Polymorphic
        """
        if data.get('type') == "Component":
            self.Meta.model = Component
            return ComponentSerializer(context=self.context).to_internal_value(data)
        if data.get('type') == "Machine":
            self.Meta.model = Machine
            return MachineSerializer(context=self.context).to_internal_value(data)
        if data.get('type') == "Tool":
            self.Meta.model = Tool
            return ToolSerializer(context=self.context).to_internal_value(data)
        if data.get('type') == "Book":
            self.Meta.model = Book
            return BookSerializer(context=self.context).to_internal_value(data)
        self.Meta.model = Element
        return super(ElementSerializer, self).to_internal_value(data)

    def create(self, validated_data):

        if self.context['request'].data.get('type') == "Component":
            self.Meta.model = Component
            return ComponentSerializer(context=self.context).create(validated_data)
        if self.context['request'].data.get('type') == "Machine":
            self.Meta.model = Machine
            return MachineSerializer(context=self.context).create(validated_data)
        if self.context['request'].data.get('type') == "Tool":
            self.Meta.model = Tool
            return ToolSerializer(context=self.context).create(validated_data)
        if self.context['request'].data.get('type') == "Book":
            self.Meta.model = Book
            return BookSerializer(context=self.context).create(validated_data)
        raise serializers.ValidationError('Unknown or missing type.')