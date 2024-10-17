from django.urls import path
from qyfy.views import LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Your existing paths
    path('api/login/', LoginView.as_view(), name='login'),  # your existing login view if using token auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]
