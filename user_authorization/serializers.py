from rest_framework import serializers
from .models import AdvancedUser, Profile

class AdvancedUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return AdvancedUser.objects.create_user(**validated_data)