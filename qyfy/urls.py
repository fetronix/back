from django.urls import path, include
from rest_framework.routers import DefaultRouter
from qyfy.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    # Your existing paths
    path('api/login/', LoginView.as_view(), name='login'),  # your existing login view if using token auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    
    path('api/assets/', AssetsListView.as_view(), name='assets-list'),
    path('api/delivery/', DeliveryListView.as_view(), name='delivery-list'),
    path('assets/', AssetNewCreateView.as_view(), name='asset-create'),
    path('assets/new/', AssetNewCreateView.as_view(), name='asset-create'),
    path('delivery/new/', DeliveryNewCreateView.as_view(), name='delivery-create'),
    path('assets/<int:pk>/', AssetsUpdateView.as_view(), name='asset-update'),
    path('assets/<int:pk>/delete/', AssetsDeleteView.as_view(), name='asset-delete'),
    
    path('api/', include(router.urls)),
 
    path('cart/add/<int:asset_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:asset_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    
]
