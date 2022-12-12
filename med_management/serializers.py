from rest_framework import serializers
# from user_authorization.views import AdvancedUserSerializer
from .models import Hospital, Appointment, Medical_history
from user_authorization.models import AdvancedUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvancedUser
        fields = ('first_name', 'last_name', 'email')

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('id', 'name', 'address', 'phone_number', 'rating')


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        # fields = ('id', 'appointment_reason', 'appointment_date', 'appointment_status')
        exclude = ('id', 'patient')
    def update(self, instance:Appointment, validated_data):

        instance.appointment_reason = validated_data.get('appointment_reason')
        instance.appointment_date = validated_data.get('appointment_date')
        instance.appointment_status = validated_data.get('appointment_status')
        instance.doctor = validated_data.get('doctor')
        instance.save()
        return instance
    
    def create(self, validated_data):
        appointment = Appointment.objects.create(
            appointment_reason = validated_data.get('appointment_reason'),
            appointment_date = validated_data.get('appointment_date'),
            appointment_status = validated_data.get('appointment_status')
        )

        return appointment

class DoctorAppointmentSerializer(serializers.ModelSerializer):
    # patient_first_name = serializers.CharField(source='patient.first_name', read_only=True)
    # patient_last_name = serializers.CharField(source='patient.last_name', read_only=True)
    # patient_email = serializers.EmailField(source='patient.email', read_only=True)
    patient = UserSerializer()
    class Meta:
        model = Appointment
        fields = ('id', 'patient', 
            'appointment_reason', 'appointment_date', 'appointment_status')
    

class PatientAppointmentSerializer(serializers.ModelSerializer):
#     doctor_first_name = serializers.CharField(source='doctor.first_name')
#     doctor_last_name = serializers.CharField(source='doctor.last_name')
#     doctor_email = serializers.EmailField(source='doctor.email')
    doctor = UserSerializer()
    class Meta:
        model = Appointment
        fields = ('id', 'doctor', 
            'appointment_reason', 'appointment_date', 'appointment_status')

class Medical_historySerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical_history
        fields = ('id', 'date_of_record', 'symptoms', 'diagnosis')


