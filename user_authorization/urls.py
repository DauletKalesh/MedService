from django.urls import path
from .views import AdvancedUserViewSet, LoginView, ProfileView

urlpatterns = [
    path('registration', AdvancedUserViewSet.as_view({'post': 'create'})),
    path('login', LoginView.as_view()),
    path('profile/<int:pk>', ProfileView.as_view())
]