from rest_framework import serializers
# from user_authorization import serializers as auth_serializer
from .models import Hospital, Appointment, Medical_history


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('id', 'name', 'address', 'phone_number', 'rating')


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ('id', 'appointment_reason', 'appointment_date', 'appointment_status')

# class DoctorAppointmentSerializer(serializers.ModelSerializer):
#     patient_first_name = serializers.CharField(source='patient.first_name', read_only=True)
#     patient_last_name = serializers.CharField(source='patient.last_name', read_only=True)
#     patient_email = serializers.EmailField(source='patient.email', read_only=True)
#     class Meta:
#         model = Appointment
#         fields = ('id', 'patient_first_name', "patient_last_name", "patient_email",
#             'appointment_reason', 'appointment_date', 'appointment_status')

# class PatientAppointmentSerializer(serializers.ModelSerializer):
#     doctor_first_name = serializers.CharField(source='doctor.first_name')
#     doctor_last_name = serializers.CharField(source='doctor.last_name')
#     doctor_email = serializers.EmailField(source='doctor.email')
#     class Meta:
#         model = Appointment
#         fields = ('id', 'doctor_first_name', "doctor_last_name", "doctor_email",
#             'appointment_reason', 'appointment_date', 'appointment_status')

class Medical_historySerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical_history
        fields = ('id', 'date_of_record', 'symptoms', 'diagnosis')


