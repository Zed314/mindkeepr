from rest_framework import serializers

from ..user import UserSerializer
from Mindkeepr.models.events import Event
from ..serializer_factory import SerializerFactory

class EventFieldMixin(serializers.Serializer):
    recording_date = serializers.ReadOnlyField()
    creator = UserSerializer(read_only=True, default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))


class EventSerializer(SerializerFactory, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = ("id", "type", "recording_date", "creator", "comment")
        depth = 1
        extra_kwargs = {
            "type": {
                "read_only": False,
            }
        }
        ordering=["-recording_date"]

    def to_representation(self, obj):
        """
        Because Event is Polymorphic
        """
        type = obj.__class__.__name__
        serializer = SerializerFactory.create_serializer(type, context=self.context)
        if(serializer):
            return serializer.to_representation(obj)
        # Should not occur
        return super(EventSerializer, self).to_representation(obj)

    def to_internal_value(self, data):
        """
        Because Event is Polymorphic
        """
        type = data.get('type')
        serializer = SerializerFactory.create_serializer(type,context=self.context)
        if(serializer):
            return serializer.to_internal_value(data)
        return super(EventSerializer, self).to_internal_value(data)

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
