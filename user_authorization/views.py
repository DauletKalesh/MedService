from rest_framework import generics, mixins, viewsets, status
from rest_framework.views import Response, APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsProfileOwner
from .serializers import AdvancedUserSerializer, ProfileSerializer
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import *
# Create your views here.

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class AdvanscedUserViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = AdvancedUserSerializer

    def create(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    # lookup_field = 'user__pk'
    lookup_url_kwarg = 'user__pk'
    permission_classes = [IsAuthenticated()]

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.request.method == 'PUT':
            permission_classes.append(IsProfileOwner())
        return permission_classes
    
    def retrieve(self, request, *args, **kwargs):
        print(request.user, request.user.id)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance.user.is_doctor:
            serializer.data.pop('patient_detail', None)
        if instance.user.is_patient:
            serializer.data.pop('patient_detail', None)
        return Response(serializer.data)
