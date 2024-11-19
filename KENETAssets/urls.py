from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'mydeliveries', DeliveryViewSet)
router.register(r'users', UserViewSet)
router.register(r'user-checkouts', UserCheckoutSet, basename='user-checkouts')

handler404 = 'KENETAssets.views.custom_404'
handler500 = 'KENETAssets.views.custom_505'


urlpatterns = [
    
    path('api/login/', LoginView.as_view(), name='login'),  # your existing login view if using token auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    
    path('api/assets/', AssetsListView.as_view(), name='assets-list'),
    path('location/create_or_update/', create_or_update_location, name='create_or_update_location'),
    path('api/delivery/', DeliveryListView.as_view(), name='delivery-list'),
    path('assets/', AssetNewCreateView.as_view(), name='asset-create'),
    path('assets/new/', AssetNewCreateView.as_view(), name='asset-create'),
    path('delivery/new/', DeliveryNewCreateView.as_view(), name='delivery-create'),
    path('assets/<int:pk>/', AssetsUpdateView.as_view(), name='asset-update'),
    path('assets/<int:pk>/delete/', AssetsDeleteView.as_view(), name='asset-delete'),
    
    path('api/', include(router.urls)),
 
    path('cart/add/<int:asset_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:asset_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/', CartListView.as_view(), name='cart-list'),  

    
    path('checkout/', CheckoutCreateView.as_view(), name='checkout-create'),
    path('checkouts/', CheckoutListView.as_view(), name='checkout-list'),
    path('checkoutsadmin/', CheckoutAdminListView.as_view(), name='checkout-list'),
    path('checkout/<int:checkout_id>/approve/', ApproveCheckoutView.as_view(), name='checkout-approve'),
    path('checkout/<int:checkout_id>/reject/', RejectCheckoutView.as_view(), name='checkout-reject'),
    path('checkout/<int:pk>/update/', CheckoutUpdateView.as_view(), name='checkout-update'),
    path('checkout/<int:pk>/update/user/', CheckoutUSerUpdateView.as_view(), name='checkout-update-user'),
    path('checkout/<int:pk>/', CheckoutDetailView.as_view(), name='checkout-detail'), 
    
    path('logingorm/', login_view, name='login-form'),
    path('logout/', logout_view, name='logout'),
    path('kenet-release-form/', kenet_release_form_view, name='kenet_release_form'),
    path('assets/<int:asset_id>/return_faulty/', ReturnFaultyAssetView.as_view(), name='return-faulty-asset'),
    path('assets/<int:asset_id>/return_decommissioned/', ReturnDecomissionedAssetView.as_view(), name='return-decommissioned-asset'),
    
    
]
