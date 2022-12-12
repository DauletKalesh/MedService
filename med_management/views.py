from django.shortcuts import render
import json
from django.http.response import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from rest_framework.viewsets import ModelViewSet
# Create your views here.

@csrf_exempt
def show_appointments(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist as e:
        return JsonResponse({'message': str(e)})
    if request.method == 'GET':
        return JsonResponse(appointment.to_json())
    elif request.method == 'PUT':
        data = json.loads(request.body)
        appointment.appointment_reason = data['appointment_reason']
        appointment.appointment_date = data['appointment_date']
        appointment.appointment_status = data['appointment_status']
        appointment.save()
        return JsonResponse(appointment.to_json())
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            comment = Appointment.objects.create(appointment_reason=data['appointment_reason'], appointment_date=data['appointment_date'], appointment_status=data['appointment_status'])
        except Exception as e:
            return JsonResponse({'message': str(e)})
        return JsonResponse(comment.to_json())
    elif request.method == 'DELETE':
        appointment.delete()
        return JsonResponse({'message': 'deleted'}, status=204)


def show_hospital(request):
    hospitals = Hospital.objects.all()
    serializer = HospitalSerializer(hospitals, many=True)
    return JsonResponse(serializer.data, safe=False)


def show_medical_history(request):
    medical_histories = Medical_history.objects.all()
    serializer = Medical_historySerializer(medical_histories, many=True)
    return JsonResponse(serializer.data, safe=False)

class AppointmentApiView(ModelViewSet):
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        if self.request.user.is_doctor:
            return self.request.user.doctor_appointments.all()
        elif self.request.user.is_patient:
            return self.request.user.patient_appointments.all()
    def perform_create(self, serializer):
        instance = serializer.save()
        if self.request.user.is_patient:
            instance.patient = self.request.user
            instance.save()
    def get_serializer(self, *args, **kwargs):
        if self.request.user.is_doctor:
            return DoctorAppointmentSerializer
        elif self.request.user.is_patient:
            return PatientAppointmentSerializer
        return self.serializer_class

