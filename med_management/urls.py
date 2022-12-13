from django.urls import path
from .views import show_appointments, show_medical_history, show_hospital, AppointmentApiView, get_medical_history_pdf
from rest_framework.routers import  DefaultRouter

router = DefaultRouter()
router.register('appointments', AppointmentApiView, 'appointment')

urlpatterns = [
    path('hospital', show_hospital),
    path('medical_history', show_medical_history),
    # path('appointment/<int:appointment_id>', show_appointments),
    #r'^my-pdf/$', PDFView.as_view(template_name='my-pdf.html'), name='my-pdf'
    #path(r'^my-pdf/$', PDFView.as_view(template_name='basic-template.html'), name='my-pdf')
    path('medhistory/to_pdf/<int:uid>', get_medical_history_pdf)
] + router.urls