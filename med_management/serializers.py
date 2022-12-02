from rest_framework import serializers

from models import Hospital, Appointment, Medical_history


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('id', 'name', 'address', 'phone_number', 'rating')


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'appointment_reason', 'appointment_date', 'appointment_status')


class Medical_historySerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical_history
        fields = ('id', 'date_of_record', 'symptoms', 'diagnosis')


