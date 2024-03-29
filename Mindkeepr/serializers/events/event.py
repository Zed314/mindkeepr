from rest_framework import serializers

from ..user import UserSerializerShort
from Mindkeepr.models.events import Event
from ..serializer_factory import SerializerFactory

class EventFieldMixin(serializers.Serializer):
    recording_date = serializers.ReadOnlyField()
    creator = UserSerializerShort(read_only=True, default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))

    def add_event_read_only_default_fields(self, validated_data):
        # Include default for read_only `creator` field
        # for some reason, it is not possible to have read only and default value https://www.django-rest-framework.org/community/release-notes/#380
        # https://stackoverflow.com/questions/35518273/how-to-set-current-user-to-user-field-in-django-rest-framework
        #print(self.fields["creator"].get_default())
        validated_data["creator"] = self.fields["creator"].get_default()

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
