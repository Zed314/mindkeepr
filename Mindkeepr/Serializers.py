from django.contrib.auth.models import User

from Mindkeepr.event_serializers import (BorrowEventSerializer,
                                          BuyEventSerializer,
                                          ConsumeEventSerializer,
                                          MaintenanceEventSerializer,
                                          IncidentEventSerializer,
                                          SellEventSerializer,
                                          UseEventSerializer,
                                          UserSerializer,
                                          ElementShortSerializer)
from Mindkeepr.models import (Attribute, Category, Component, Element,
                               Location, Machine, Tool, Book, StockRepartition,
                               BorrowEvent, Event,Project)
from rest_framework import serializers

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class UserDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ordering = ['-id']
        fields = ("id", "first_name", "last_name", "email", "projects")
        depth = 1

class LocationSerializerShort(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    url = serializers.HyperlinkedIdentityField(view_name="location-detail", lookup_field='pk')
    nb_children = serializers.IntegerField(read_only=True)
    class Meta:
        model = Location
        fields = ("id", "name","url","nb_children")
        depth = 2

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    manager = UserSerializer()
    class Meta:
        model = Project
        fields = ("id", "name","description","manager")
        depth = 2



class LocationFullSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)

    children = RecursiveField(many=True,required=False)
    class Meta:
        model = Location
        fields = ("id", "name","children")

class LocationSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(required=False)
    parent = LocationSerializerShort()
    children = LocationSerializerShort(many=True,required=False)
    class Meta:
        model = Location
        fields = ("id", "name", "description","parent","children")
        depth = 2


class AttributeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Attribute
        fields = ("id", "name", "value")
        depth = 2


class StockRepartitionSerializer(serializers.HyperlinkedModelSerializer):

    location = LocationSerializer()
    project = ProjectSerializer()
    element = ElementShortSerializer()
    class Meta:
        model = StockRepartition
        fields = ("id", "quantity", "location", "project","element", "status")
        depth = 2


class SubCategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="category-detail", lookup_field='pk')
    nb_children = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'url','nb_children')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    parent = SubCategorySerializer(required=True)
    children = SubCategorySerializer(many=True,required=False)
    class Meta:
        model = Category
        fields = ("id", "name","parent","children")


class CategorySerializerFull(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    children = RecursiveField(many=True,required=False)
    class Meta:
        model = Category
        fields = ("id", "name","parent","children")

class CategoryIdSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id']

class CategorySerializerShortShort(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Category
        fields = ["id"]

class CategorySerializerShort(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    parent = CategoryIdSerializerFull(required=True)
    class Meta:
        model = Category
        fields = ("id", "name","parent")

class ElementMinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Element
        fields = ("id", "name")

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

#class BorrowingSerializer(serializers.HyperlinkedModelSerializer):
#    id = serializers.IntegerField()
#
#    location_source = LocationSerializer()
#    element = ElementMinSerializer()
#
#    class Meta:
#        model = BorrowEvent
#        depth = 1
#        fields = ("id", "quantity", "recording_date", "scheduled_return_date",
#                  "location_source",
#                  "element",
#                  "comment")

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


class MachineSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):

    maintenance_history = MaintenanceEventSerializer(many=True, read_only=True)
    #def get_status_name(self, obj):
     #   return obj.get_status_display()
    #status = serializers.SerializerMethodField(read_only=True, source='get_status_name')
    status= serializers.CharField(
        source='get_status_display',read_only=True
    )
    class Meta:
        model = Machine
        fields = ElementSerializer.Meta.fields + ("maintenance_history","status")
        depth = 1

    def create(self, validated_data):
        category = self.get_category(validated_data)
        machine = Machine.objects.create(**validated_data,**category)
        return machine


class ToolSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Tool
        fields = ElementSerializer.Meta.fields
        depth = 1

    def create(self, validated_data):
        category = self.get_category(validated_data)
        tool = Tool.objects.create(**validated_data,**category)
        return tool


class BookSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Book
        fields = ElementSerializer.Meta.fields
        depth = 1

    def create(self, validated_data):
        category = self.get_category(validated_data)
        book = Book.objects.create(**validated_data, **category)
        return book


class ComponentSerializer(ElementFieldMixin, serializers.HyperlinkedModelSerializer):
    attributes = AttributeSerializer(many=True, required=False)

    class Meta:
        model = Component
        fields = ElementSerializer.Meta.fields + ('attributes',"datasheet")
        depth = 1

    def create(self, validated_data):
        category = self.get_category(validated_data)
        component = Component.objects.create(
            **validated_data, **category)#, category=category)
        return component
