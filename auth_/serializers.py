from rest_framework import serializers
from .models import AdvancedUser, Profile

class AdvancedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvancedUser
        fields = '__all__'
    
    def create(self, validated_data):
        return AdvancedUser.objects.create_user(self.initial_data.get('roles'), **validated_data)