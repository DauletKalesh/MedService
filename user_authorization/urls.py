from django.urls import path
from .views import AdvancedUserViewSet, LoginView

urlpatterns = [
    path('registration', AdvancedUserViewSet.as_view({'post': 'create'})),
    path('login', LoginView.as_view()),
]