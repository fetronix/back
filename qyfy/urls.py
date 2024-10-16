
from django.urls import path
from .views import *

urlpatterns = [
    path('assets/', AssetCreateView.as_view(), name='assets-list-create'),
    path('assets/view', AssetsViewListCreate.as_view(), name='assets-list-create'),
    
    path('category/view', CategoryListCreate.as_view(), name='category-list-create'),
    path('category/', CategoryListCreate.as_view(), name='category-list-create'),
    
    path('location/view', LocationListCreate.as_view(), name='location-list-create'),
    path('location/', LocationListCreate.as_view(), name='location-list-create'),
    
    path('assets/export/', AssetsExportView.as_view(), name='assets-export'),
    
    path('assets/all/', assets_list, name='assets-list'),  # New URL for viewing assets
    
    path('deliveries/', DeliveryListCreateAPIView.as_view(), name='delivery-list-create'),
  
    path('assets/<int:pk>/', AssetUpdateView.as_view(), name='asset-update'),  # Update asset by ID
    
    path('login/', LoginView.as_view(), name='login'),
]
