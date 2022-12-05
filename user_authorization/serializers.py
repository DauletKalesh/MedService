from rest_framework import serializers
from .models import AdvancedUser, Profile, ProfileDetail
from med_management.serializers import Medical_historySerializer

class AdvancedUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return AdvancedUser.objects.create_user(**validated_data)

class DoctorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileDetail
        fields = ( 'hospital', 'specialization', 'license_file')

class PatientDetailSerializer(serializers.ModelSerializer):

    med_history = Medical_historySerializer(many=True)

    class Meta:
        model = ProfileDetail
        fields = ( 'iin', 'med_history',)

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user.username')
    first_name = serializers.StringRelatedField(source='user.first_name')
    last_name = serializers.StringRelatedField(source='user.last_name')
    patient_detail = PatientDetailSerializer(source='detail')
    doctor_detail = DoctorDetailSerializer(source='detail')

    class Meta:
        model = Profile
        exclude = ('detail', 'id')
