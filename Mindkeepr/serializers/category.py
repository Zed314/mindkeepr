from rest_framework import serializers
from Mindkeepr.models import Category

from .fields import RecursiveField

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