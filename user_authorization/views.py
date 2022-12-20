from rest_framework import generics, mixins, viewsets, status
from rest_framework.views import Response, APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsProfileOwner
from .serializers import AdvancedUserSerializer, DoctorProfileSerializer,\
            PatientProfileSerializer
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import *
from .tasks import send_email_notification
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http.request import HttpRequest
import logging
# Create your views here.

logger = logging.getLogger(__name__)
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


def send_verification(serializer):
    num = random.randint(100000, 999999)
    send_mail(
                subject='Registration code',
                message='Please write this code in form! {}'.format(num),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[serializer.email])
    


class AdvanscedUserViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = AdvancedUserSerializer

    def create(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_email_notification.delay(
                subject='Registration success',
                message='You are registered!',
                recipient_list=[request.data.get('email')])
            logger.info(f"{request.data.get('username')} succesfully registered")
            return Response({"message": "Account succesfully created"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def retrieve(self, request, id):
    #     ser

class LoginView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email, password)
        try:
            user = AdvancedUser.objects.get(email=email)
        except:
            return Response({'message': 'Wrong email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        if user:
            if user.is_blocked:
                return Response(
                    {'message': 'Account is blocked. Contact with admin to unblock.'}, 
                    status=401)
            if user.login_attempts >= 3:
                user.is_blocked = True
                user.save()
                return Response(
                    {'message': 'Too many attempts, account is blocked. Contact with admin.'}, 
                    status=401)
            if not check_password(password, user.password):
                user.login_attempts += 1
                user.save()
                return Response({'message': 'Wrong email or password'}, status=status.HTTP_401_UNAUTHORIZED)

            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                user = serializer.object.get('user') or request.user
                token = serializer.object.get('token')
                response_data = jwt_response_payload_handler(token, user, request)
                response = Response(response_data)
                if api_settings.JWT_AUTH_COOKIE:
                    expiration = (datetime.utcnow() +
                                api_settings.JWT_EXPIRATION_DELTA)
                    response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                        token,
                                        expires=expiration,
                                        httponly=True)
                return response

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    # lookup_field = 'user__pk'
    lookup_url_kwarg = 'user__pk'
    permission_classes = [IsAuthenticated()]

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.request.method == 'PUT':
            permission_classes.append(IsProfileOwner())
        return permission_classes
    
    def get_serializer(self, instance):
        if instance.user.is_doctor:
            return DoctorProfileSerializer(instance)
        return PatientProfileSerializer(instance)
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # if instance.user.is_doctor:
        #     del data['patient_detail']
        # if instance.user.is_patient:
        #     del data['doctor_detail']
        return Response(data)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.is_doctor:
            serializer = DoctorProfileSerializer(instance=instance, data=request.data)
        else:
            serializer = PatientProfileSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logger.info(f"{request.data.get('username')} profile updated response - {serializer.data}")
            return Response({'message': 'updated'})
        print(serializer.errors)
        return Response({'message': 'wrong datas'}, status=status.HTTP_400_BAD_REQUEST)
