
from django.urls import path
from .views import *

urlpatterns = [
    path('assets/', AssetsListCreate.as_view(), name='assets-list-create'),
    path('assets/view', AssetsListCreate.as_view(), name='assets-list-create'),
    
    path('category/view', CategoryListCreate.as_view(), name='category-list-create'),
    path('category/', CategoryListCreate.as_view(), name='category-list-create'),
    
    path('assets/export/', AssetsExportView.as_view(), name='assets-export'),
    
    path('assets/all/', assets_list, name='assets-list'),  # New URL for viewing assets
]
