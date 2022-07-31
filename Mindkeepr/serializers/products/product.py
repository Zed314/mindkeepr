from rest_framework import serializers

from Mindkeepr.models.products.product import Product
from ..serializer_factory import SerializerFactory

class ProductSerializer(serializers.HyperlinkedModelSerializer, SerializerFactory):

    class Meta:
        model = Product
        fields = ["id", "title", "type", "image", "short_description","is_new"]
        depth = 2
        extra_kwargs = {
            "type": {
                "read_only": False
            }
        }


    def to_representation(self, obj):
        """
        Because Product is Polymorphic
        """
        type = obj.__class__.__name__
        serializer = SerializerFactory.create_serializer(type, context=self.context)
        if(serializer):
            return serializer.to_representation(obj)
        # Should not occur
        return super(ProductSerializer, self).to_representation(obj)

    def to_internal_value(self, data):
        """
        Because Product is Polymorphic
        """
        type = data.get('type')
        serializer = SerializerFactory.create_serializer(type,context=self.context)
        if(serializer):
            return serializer.to_internal_value(data)
        return super(ProductSerializer, self).to_internal_value(data)

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