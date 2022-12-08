from django.urls import path
from .views import show_appointments, show_medical_history, show_hospital, AppointmentApiView
from rest_framework.routers import  DefaultRouter

router = DefaultRouter()
router.register('appointments', AppointmentApiView, 'appointment')

urlpatterns = [
    path('hospital', show_hospital),
    path('medical_history', show_medical_history),
    # path('appointment/<int:appointment_id>', show_appointments),
] + router.urls