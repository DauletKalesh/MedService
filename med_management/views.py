from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, permissions, views, mixins, viewsets
from user_authorization.permissions import IsPatient
from user_authorization.models import * 
from .serializers import *
from .models import *
import json
from datetime import datetime
from .pdf_service import create_pdf
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
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


class HospitalViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [permissions.IsAdminUser, ]

# def show_hospital(request):
#     hospitals = Hospital.objects.all()
#     serializer = HospitalSerializer(hospitals, many=True)
#     return JsonResponse(serializer.data, safe=False)

class MedHistoryViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Medical_history.objects.all()
    serializer_class = Medical_historySerializer
    permission_classes = [permissions.IsAdminUser, ]

# def show_medical_history(request):
#     medical_histories = Medical_history.objects.all()
#     serializer = Medical_historySerializer(medical_histories, many=True)
#     return JsonResponse(serializer.data, safe=False)

def get_medical_history_pdf(request, uid):
    if request.method == 'GET':
        user_data = Profile.objects.get(id=uid)
        pdfstr = create_pdf(user_data)
        response = HttpResponse(content_type='application/pdf')
        response.write(pdfstr)
        response['Content-Disposition'] = 'filename=med_history_{}.pdf'.format(uid)
        return response


class SpecializationAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(cache_page(60*60))
    def get(self, request):
        specialization = Specialization.objects.all()
        serializer = SpecializationSerializer(instance=specialization, many=True)
        return Response(serializer.data)




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
    def get_serializer_class(self):
        if self.request.user.is_doctor:
            return DoctorAppointmentSerializer
        elif self.request.user.is_patient:
            return PatientAppointmentSerializer
        return self.serializer_class


class CommentApiView(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsPatient]
    queryset = Comment.objects.all()

    def list(self, request):
        queryset = Comment.objects.all().filter(author=request.user)
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


