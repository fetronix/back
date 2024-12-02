from django.urls import path
from .views import get_latest_version

urlpatterns = [
    path('latest_version/', get_latest_version, name='get_latest_version'),
]
