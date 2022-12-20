from django.urls import path
from .views import show_appointments, AppointmentApiView, \
    CommentApiView,get_medical_history_pdf, SpecializationAPIView, HospitalViewSet,\
        MedHistoryViewSet
from rest_framework.routers import  DefaultRouter

router = DefaultRouter()
router.register('appointments', AppointmentApiView, 'appointment')

router.register('hospitals', HospitalViewSet, basename='hospitals')
router.register('medical_history', MedHistoryViewSet, basename='medical_history')

urlpatterns = [
    # path('hospital', show_hospital),
    # path('medical_history', show_medical_history),
    path('comments', CommentApiView.as_view({'get':'list',
                                             'post':'post'})),
    path('comments/<int:h_id>', CommentApiView.as_view({'get':'list_by_hospital'})),
    path('comments/<int:pk>', CommentApiView.as_view({'put':'put',
                                                    'delete':'delete'})),
    # path('appointment/<int:appointment_id>', show_appointments),n                            

    # path('appointment/<int:appointment_id>', show_appointments),
    #r'^my-pdf/$', PDFView.as_view(template_name='my-pdf.html'), name='my-pdf'
    #path(r'^my-pdf/$', PDFView.as_view(template_name='basic-template.html'), name='my-pdf')
    path('medhistory/to_pdf/<int:uid>', get_medical_history_pdf),
    path('specializations', SpecializationAPIView.as_view())
] + router.urls