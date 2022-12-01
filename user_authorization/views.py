from django.shortcuts import render
from rest_framework import generics, mixins, viewsets, status
from rest_framework.views import Response, APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import AdvancedUserSerializer
from .models import *
# Create your views here.

class AdvancedUserViewSet(viewsets.ViewSet):
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
