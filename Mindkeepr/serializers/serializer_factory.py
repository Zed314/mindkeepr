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