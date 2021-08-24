from rest_framework import serializers
from Mindkeepr.models import Project
from .user import UserSerializer

class ProjectShortSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Project
        fields = ["id"]

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    manager = UserSerializer()
    class Meta:
        model = Project
        fields = ("id", "name","description","manager")
        depth = 2
