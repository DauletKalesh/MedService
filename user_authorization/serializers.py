from rest_framework import serializers
from .models import AdvancedUser, Profile, ProfileDetail
from med_management.serializers import Medical_historySerializer
from med_management.models import Hospital, Specialization

class AdvancedUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        return AdvancedUser.objects.create_user(**validated_data)

class DoctorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileDetail
        fields = ( 'hospital', 'specialization', 'license_file')

class PatientDetailSerializer(serializers.ModelSerializer):

    med_history = Medical_historySerializer(many=True, required=False)

    class Meta:
        model = ProfileDetail
        fields = ( 'iin', 'med_history',)

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user.username')
    first_name = serializers.StringRelatedField(source='user.first_name')
    last_name = serializers.StringRelatedField(source='user.last_name')
    patient_detail = PatientDetailSerializer(source='detail', read_only=True)
    doctor_detail = DoctorDetailSerializer(source='detail', read_only=True)

    class Meta:
        model = Profile
        exclude = ('detail', 'id', 'user')
        extra_kwargs = {'username': {"required": False, "allow_null": True},
                        'first_name': {"required": False, "allow_null": True},
                        'last_name': {"required": False, "allow_null": True},
                        'avatar': {"required": False, "allow_null": True},
                        'iin': {"required": False, "allow_null": True},
                        }
    
    def update(self, instance:Profile, validated_data):

        instance.user.username = validated_data.get('username')
        instance.user.first_name = validated_data.get('first_name')
        instance.user.last_name = validated_data.get('last_name')

        if patient_detail:=validated_data.get('patient_detail'):
            instance.detail.iin = patient_detail.get('iin')
        
        if doctor_detail:=validated_data.get('doctor_detail'):
            try:
                instance.detail.hospital = Hospital.objects.get(
                    pk=doctor_detail.get('hospital'))
            except:
                instance.detail.hospital = None
            
            try:
                instance.detail.specialization = Specialization.objects.get(
                    pk=doctor_detail.get('specialization'))
            except:
                instance.detail.specialization = None
            instance.detail.license_file = doctor_detail.get('license_file')
        instance.birthday =  validated_data.get("birthday")
        instance.gender = validated_data.get("gender")
        instance.avatar = validated_data.get('avatar')

        return super().update(instance, validated_data)
