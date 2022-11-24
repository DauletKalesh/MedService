from django.shortcuts import render
from rest_framework import generics, mixins, viewsets, status
from rest_framework.views import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import AdvancedUserSerializer
# Create your views here.

class UserViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = AdvancedUserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)