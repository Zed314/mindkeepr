from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
      class Meta:
          model = User
          fields = ('id', 'username',"first_name","last_name","get_full_name","email")

class UserSerializerShort(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = User
        fields = ['id']

class UserDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ordering = ['-id']
        fields = ("id", "first_name", "last_name", "email", "projects")
        depth = 1