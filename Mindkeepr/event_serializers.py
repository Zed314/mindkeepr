from Mindkeepr.models import Event, BuyEvent, UseEvent, SellEvent, ConsumeEvent, ReturnEvent, BorrowEvent, MaintenanceEvent, IncidentEvent, MoveEvent, UnUseEvent
from Mindkeepr.models import Component, Location, StockRepartition, Element, Machine, Project
from django.contrib.auth.models import User
from rest_framework import serializers
from typing import Callable

class SerializerFactory:
    """ The factory class for creating serializers"""

    registry = {}
    """ Internal registry for available serializers """

    @classmethod
    def register(cls, name: str) -> Callable:

        def inner_wrapper(wrapped_class: serializers.HyperlinkedModelSerializer) -> Callable:
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def create_serializer(cls, name: str, **kwargs) -> 'ExecutorBase':

        if name not in cls.registry:
            return None

        ser_class = cls.registry[name]
        serializer = ser_class(**kwargs)
        return serializer


class ProjectShortSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Project
        fields = ["id"]


class ElementShortSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    class Meta:
        model = Element
        fields = ("id", "type", "name")
        depth = 2
        extra_kwargs = {
            "type": {
                "read_only": False
            }
        }

class LocationShortSerializer(serializers.HyperlinkedModelSerializer):
    # Otherwise cannot be seen by other on updates/create
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Location
        fields = ["id", "name"]
        depth = 2

class EventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = ("id", "type", "recording_date","creator", "comment")
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


class UserSerializer(serializers.ModelSerializer):
      class Meta:
          model = User
          fields = ('id', 'username',"first_name","last_name","get_full_name","email")

class UserSerializerShort(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = User
        fields = ['id']

class EventFieldMixin(serializers.Serializer):
    recording_date = serializers.ReadOnlyField()
    creator = UserSerializer(read_only=True, default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))

@SerializerFactory.register('SellEvent')
class SellEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    element = ElementShortSerializer()
    location_source = LocationShortSerializer()

    class Meta:
        model = SellEvent
        fields = EventSerializer.Meta.fields + ("element",
                  "quantity", "price", "location_source")
        depth = 1
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        sell_event = SellEvent(
            **validated_data, element=element, location_source=location)
        if sell_event.is_add_to_element_possible():
            sell_event.save()
            return sell_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')

@SerializerFactory.register('BuyEvent')
class BuyEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    element = ElementShortSerializer()
    location_destination = LocationShortSerializer()
    project = ProjectShortSerializer(required=False)

    class Meta:
        model = BuyEvent
        fields = EventSerializer.Meta.fields + ("element",
                  "price", "supplier", "quantity", "location_destination","project")
        depth = 1
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location = Location.objects.get(
            id=validated_data.pop('location_destination')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        buy_event = BuyEvent(
            **validated_data, element=element, location_destination=location)
        if buy_event.is_add_to_element_possible():
            buy_event.save()
            return buy_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')

@SerializerFactory.register('UseEvent')
class UseEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    location_destination = LocationShortSerializer()
    location_source = LocationShortSerializer()
    element = ElementShortSerializer()
    project = ProjectShortSerializer()

    class Meta:
        model = UseEvent
        fields = EventSerializer.Meta.fields + ("element", "quantity",
                  "location_destination", "location_source","project")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location_source = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        location_destination = Location.objects.get(
            id=validated_data.pop('location_destination')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        project = Project.objects.get(id=validated_data.pop('project')["id"])
        use_event = UseEvent(**validated_data, element=element, project=project,
                             location_source=location_source, location_destination=location_destination)
        if use_event.is_add_to_element_possible():
            use_event.save()
            return use_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')


@SerializerFactory.register('UnUseEvent')
class UnUseEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    location_destination = LocationShortSerializer()
    location_source = LocationShortSerializer()
    element = ElementShortSerializer()

    class Meta:
        model = UnUseEvent
        fields = EventSerializer.Meta.fields + ("element", "quantity",
                  "location_destination", "location_source")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location_source = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        location_destination = Location.objects.get(
            id=validated_data.pop('location_destination')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        unuse_event = UnUseEvent(**validated_data, element=element,
                                  location_source=location_source, location_destination=location_destination)
        if unuse_event.is_add_to_element_possible():
            unuse_event.save()
            return unuse_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')

class ReturnEventSerializerShort(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    location_destination = LocationShortSerializer()

    is_date_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = ReturnEvent
        fields = EventSerializer.Meta.fields + ("is_date_overdue",
                   "location_destination")
        depth = 2
        ordering = EventSerializer.Meta.ordering

@SerializerFactory.register('BorrowEvent')
class BorrowEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    location_source = LocationShortSerializer()
    element = ElementShortSerializer()
    is_returned = serializers.ReadOnlyField()
    return_event = ReturnEventSerializerShort(required=False)
    class Meta:
        model = BorrowEvent
        fields = EventSerializer.Meta.fields + ("element", "quantity", "is_returned",
                  "scheduled_return_date", "location_source","return_event")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location_source = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        borrow_event = BorrowEvent(**validated_data, element=element,
                             location_source=location_source)
        if borrow_event.is_add_to_element_possible():
            borrow_event.save()
            return borrow_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')

class BorrowEventShortSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = BorrowEvent
        fields = ("id",)
        depth = 2

@SerializerFactory.register('ReturnEvent')
class ReturnEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):

    location_destination = LocationShortSerializer()

    borrow_associated = BorrowEventShortSerializer()
    is_date_overdue = serializers.BooleanField(read_only=True)
    element = ElementShortSerializer(read_only=True)
    class Meta:
        model = ReturnEvent
        fields = EventSerializer.Meta.fields + ("element","is_date_overdue",
                   "location_destination","borrow_associated")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location_destination= Location.objects.get(
            id=validated_data.pop('location_destination')["id"])
        borrow_event = BorrowEvent.objects.get(id=validated_data.pop('borrow_associated')["id"])

        return_event = ReturnEvent(**validated_data, borrow_associated=borrow_event,
                    location_destination=location_destination,
                    )
        if return_event.is_add_to_element_possible():
            return_event.save()
            return return_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')

@SerializerFactory.register('MaintenanceEvent')
class MaintenanceEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):
    element = ElementShortSerializer(required=False)
    assignee = UserSerializerShort(required=False)
    class Meta:
        model = MaintenanceEvent
        fields = EventSerializer.Meta.fields + ("assignee", "is_done","scheduled_date","completion_date","element")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        machine = Machine.objects.get(id=validated_data.pop('element')["id"])
        try:
            assignee = User.objects.get(id=validated_data.pop("assignee")["id"])
        except Exception:
            raise serializers.ValidationError('Missing assignee.')
        maintenance_event = MaintenanceEvent(**validated_data, element=machine, assignee=assignee)
        if maintenance_event.is_add_to_element_possible():
            maintenance_event.save()
            return maintenance_event
        else:
            raise serializers.ValidationError('Event can not be added to element.')

    def update(self, instance, validated_data):

        instance = MaintenanceEvent.objects.get(id=instance.id)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.is_done = validated_data.get('is_done', instance.is_done)
        instance.scheduled_date = validated_data.get('scheduled_date', instance.scheduled_date)
        instance.save()
        return instance

@SerializerFactory.register('ConsumeEvent')
class ConsumeEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):
    location_source = LocationShortSerializer()
    element = ElementShortSerializer()
    class Meta:
        model = ConsumeEvent
        fields = EventSerializer.Meta.fields + (
                  "quantity", "element", "location_source")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location_source = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        event = ConsumeEvent(**validated_data, element=element, location_source=location_source)
        if event.is_add_to_element_possible():
            event.save()
            return event
        else:
            raise serializers.ValidationError('Event can not be added to element.')


@SerializerFactory.register('IncidentEvent')
class IncidentEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):
    element = ElementShortSerializer()
    class Meta:
        model = IncidentEvent
        fields = EventSerializer.Meta.fields + ("element","new_status","get_new_status_display")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        element = Machine.objects.get(id=validated_data.pop('element')["id"])
        incident_event = IncidentEvent(**validated_data, element=element)
        if incident_event.is_add_to_element_possible():
            incident_event.save()
            return incident_event
        else:
            raise serializers.ValidationError('Event can not be added to element.')

@SerializerFactory.register('MoveEvent')
class MoveEventSerializer(EventFieldMixin, serializers.HyperlinkedModelSerializer):
    element = ElementShortSerializer()
    location_source = LocationShortSerializer()
    location_destination = LocationShortSerializer()
    class Meta:
        model = MoveEvent
        fields = EventSerializer.Meta.fields + ("element", "quantity",
                  "location_destination", "location_source")
        depth = 2
        ordering = EventSerializer.Meta.ordering

    def create(self, validated_data):
        location_source = Location.objects.get(
            id=validated_data.pop('location_source')["id"])
        location_destination = Location.objects.get(
            id=validated_data.pop('location_destination')["id"])
        element = Element.objects.get(id=validated_data.pop('element')["id"])
        move_event = MoveEvent(**validated_data, element=element,
                             location_source=location_source, location_destination=location_destination)
        if move_event.is_add_to_element_possible():
            move_event.save()
            return move_event
        else:
            raise serializers.ValidationError(
                'Event can not be added to element.')
