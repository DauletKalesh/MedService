from django.urls import path
from .views import show_appointments, show_medical_history, show_hospital, AppointmentApiView,\
    CommentApiView
from rest_framework.routers import  DefaultRouter

router = DefaultRouter()
router.register('appointments', AppointmentApiView, 'appointment')


urlpatterns = [
    path('hospital', show_hospital),
    path('medical_history', show_medical_history),
    path('comments', CommentApiView.as_view({'get':'list',
                                             'post':'post'})),
    path('comments/<int:h_id>', CommentApiView.as_view({'get':'list_by_hospital'})),
    path('comments/<int:pk>', CommentApiView.as_view({'put':'put',
                                                    'delete':'delete'}))
    # path('appointment/<int:appointment_id>', show_appointments),n                            
] + router.urls