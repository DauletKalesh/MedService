from django.urls import path
from .views import AdvancedUserViewSet

urlpatterns = [
    path('user', AdvancedUserViewSet.as_view({'post': 'create'})),
]