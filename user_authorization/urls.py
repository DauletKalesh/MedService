from django.urls import path
from .views import AdvanscedUserViewSet, LoginView, ProfileView


urlpatterns = [
    path('registration', AdvanscedUserViewSet.as_view({'post': 'create'})),
    path('login', LoginView.as_view()),
    path('profile/<int:user__pk>', ProfileView.as_view())
]