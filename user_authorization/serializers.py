from rest_framework import serializers
from .models import AdvancedUser, Profile
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

# class DoctorDetailSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProfileDetail
#         fields = ( 'hospital', 'specialization', 'license_file')

# class PatientDetailSerializer(serializers.ModelSerializer):

#     med_history = Medical_historySerializer(many=True, required=False)

#     class Meta:
#         model = ProfileDetail
#         fields = ( 'iin', 'med_history',)

class DoctorProfileSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user.username')
    first_name = serializers.StringRelatedField(source='user.first_name')
    last_name = serializers.StringRelatedField(source='user.last_name')

    class Meta:
        model = Profile
        exclude = ('id', 'user',)
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

        instance.iin = validated_data.get('iin')
        try:
            instance.hospital = Hospital.objects.get(
                pk=validated_data.get('hospital'))
        except Hospital.DoesNotExist:
            instance.hospital = None
        
        try:
            instance.specialization = Specialization.objects.get(
                pk=validated_data.get('specialization'))
        except Specialization.DoesNotExist:
            instance.specialization = None
        instance.license_file = validated_data.get('license_file')
        instance.birthday =  validated_data.get("birthday")
        instance.gender = validated_data.get("gender")
        instance.avatar = validated_data.get('avatar')
        instance.save()
        return instance

class PatientProfileSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user.username')
    first_name = serializers.StringRelatedField(source='user.first_name')
    last_name = serializers.StringRelatedField(source='user.last_name')
    # med_history = Medical_historySerializer(many=True)
    class Meta:
        model = Profile
        exclude = ('id', 'user', 'hospital', 'specialization', 'license_file')
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

        instance.iin = validated_data.get('iin')
        # try:
        #     instance.hospital = Hospital.objects.get(
        #         pk=validated_data.get('hospital'))
        # except Hospital.DoesNotExist:
        #     instance.hospital = None
        
        # try:
        #     instance.specialization = Specialization.objects.get(
        #         pk=validated_data.get('specialization'))
        # except Specialization.DoesNotExist:
        #     instance.specialization = None
        # instance.license_file = validated_data.get('license_file')
        instance.birthday =  validated_data.get("birthday")
        instance.gender = validated_data.get("gender")
        instance.avatar = validated_data.get('avatar')
        instance.save()
        return instance
