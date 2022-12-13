from django.shortcuts import render, get_object_or_404
import json
from django.http.response import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, permissions
from user_authorization.models import * 
import jinja2
import pdfkit
from datetime import datetime
from .pdf_service import create_pdf
from django.http import HttpResponse
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

def get_medical_history_pdf(request, uid):
    if request.method == 'GET':
        user_data = ProfileDetail.objects.get(id=uid)
        create_pdf(user_data)
        response = HttpResponse('pdf_generated.pdf', content_type='application/pdf') 
        response['Content-Disposition'] = 'filename="заявление на открытие счета.pdf"' 
        return response



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


class CommentApiView(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    queryset = queryset = Comment.objects.all()

    def list(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def list_by_hospital(self, request, h_id):
        queryset = Comment.objects.filter(hospital_id = h_id)#self.request.hospital_id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            comment_obj = self.perform_create(serializer)
            return Response({"Success": "Comment {} created!".format(comment_obj.author)})
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        serializer = CommentSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.update(Comment.objects.get(pk=pk), request.data)
        return Response({"Success": "Comment updated!"})
    
    def delete(self, request, pk):
        item = get_object_or_404(Comment, pk=pk)
        item.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
        
    def perform_create(self, serializer):
        instance = serializer.save()
        if self.request.user.is_patient:
            instance.author = self.request.user
            instance.save()
            instance.hospital.set_rating()
        return instance


