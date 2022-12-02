from django.shortcuts import render
import json
from django.http.response import JsonResponse
from models import *
from django.views.decorators.csrf import csrf_exempt
from serializers import *
# Create your views here.

@csrf_exempt
def show_appointments(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist as e:
        return JsonResponse({'message': str(e)})
    if request.method == 'GET':
        return JsonResponse(Appointment.to_json())
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
    serializer = Medical_history(medical_histories, many=True)
    return JsonResponse(serializer.data, safe=False)
