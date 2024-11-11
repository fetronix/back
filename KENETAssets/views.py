from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated  # You can use any permission class
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *  
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser

from background_task import background
from django.http import JsonResponse
from .tasks import *  # Import your background task



class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Create JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id, 
                    "username": user.username,
                    "role": user.role,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class AssetsListView(generics.ListAPIView):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access
   

class DeliveryListView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliveryListSerializer
    permission_classes = [IsAuthenticated]  

class AssetsCreateView(generics.CreateAPIView):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure authentication
    
class AssetNewCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = AssetCreateSerializer(data=request.data)
        if serializer.is_valid():
            asset = serializer.save()
            return Response(AssetsSerializer(asset).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryNewCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = DeliveryCreateSerializer(data=request.data)
        if serializer.is_valid():
            asset = serializer.save()
            return Response(DeliveryCreateSerializer(asset).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssetsUpdateView(generics.UpdateAPIView):
    queryset = Assets.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure authentication

class AssetsDeleteView(generics.DestroyAPIView):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure authentication
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer # Ensure only authenticated users can access

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer # Ensure only authenticated users 
    

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliveryListSerializer # Ensure only authenticated users 
    
    
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Suppliers.objects.all()
    serializer_class = SupplierSerializer # Ensure only authenticated users 

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    
class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, asset_id):
        user = request.user
        asset = get_object_or_404(Assets, id=asset_id)

        # Check if the asset is already in the user's cart
        if Cart.objects.filter(user=user, asset=asset).exists():
            return Response({'message': 'Item is already in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Add to cart
        cart_item = Cart(user=user, asset=asset)
        cart_item.save()

        return Response({'message': 'Added to cart'}, status=status.HTTP_201_CREATED)


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def delete(self, request, asset_id):
        user = request.user
        cart_item = get_object_or_404(Cart, id=asset_id)
        
        if cart_item:
            # Remove the item from the cart
            cart_item.delete()
            return Response({'message': 'Removed from Dispatch basket'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Item not in Dispatch basket'}, status=status.HTTP_400_BAD_REQUEST)



class CheckoutCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        # Filter cart items based on the status 'pending_release'
        cart_items = Cart.objects.filter(user=user, asset__status='pending_release')

        if not cart_items.exists():
            return Response({"detail": "No items with status 'pending_release' in your cart."}, status=status.HTTP_400_BAD_REQUEST)

        new_location = request.data.get('new_location')
        if not new_location:
            return Response({"detail": "New location is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Checkout for the current user
        checkout = Checkout.objects.create(user=user)
        checkout.cart_items.set(cart_items)
        checkout.save()

        # Update the status and location of the assets in the cart
        for cart_item in cart_items:
            asset = cart_item.asset
            asset.status = 'pending_approval'  # Update the status
            asset.new_location = new_location  # Set the new location
            asset.save()

        serializer = CheckoutSerializer(checkout)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CheckoutListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)  # Show only the user's checkouts


class CheckoutAdminListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer


class ApproveCheckoutView(APIView):
    permission_classes = [IsAdminUser]  # Only admins can approve checkouts

    def post(self, request, checkout_id, *args, **kwargs):
        try:
            checkout = Checkout.objects.get(id=checkout_id)
            cart_items = checkout.cart_items.all()

            # List to keep track of assets that couldn't be approved
            failed_assets = []

            for cart_item in cart_items:
                asset = cart_item.asset
                if asset.status == 'approved':
                    # If the asset is already approved, add to the failed_assets list
                    failed_assets.append(f"Asset {asset.serial_number} is already approved.")
                elif asset.status == 'pending_approval':
                    # Approve the asset if it's pending approval
                    asset.status = 'approved'
                    asset.save()
                    
                else:
                    # If asset status is not "pending_approval", you can either skip or handle it differently
                    failed_assets.append(f"Asset {asset.serial_number} cannot be approved due to its current status: {asset.status}.")

            # If there are no failed assets, return success
            if not failed_assets:
                save_approved_asset_movements() 
                return Response(
                    {"detail": "All assets in the checkout have been approved."},
                    status=status.HTTP_200_OK
                )

            # If there are failed assets, return a message with all the failed ones
            return Response(
                {"detail": "Some assets could not be approved.", "failed_assets": failed_assets},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Checkout.DoesNotExist:
            return Response({"detail": "Checkout not found."}, status=status.HTTP_404_NOT_FOUND)
        



class RejectCheckoutView(APIView):
    permission_classes = [IsAdminUser]  # Only admins can approve checkouts

    def post(self, request, checkout_id, *args, **kwargs):
        try:
            checkout = Checkout.objects.get(id=checkout_id)
            cart_items = checkout.cart_items.all()

            # List to keep track of assets that couldn't be approved
            failed_assets = []

            for cart_item in cart_items:
                asset = cart_item.asset
                if asset.status == 'rejected':
                    # If the asset is already rejected, add to the failed_assets list
                    failed_assets.append(f"Asset {asset.serial_number} is already rejected.")
                elif asset.status == 'pending_approval':
                    # Reject the asset if it's pending approval
                    asset.status = 'rejected'
                    asset.save()
                else:
                    # If asset status is not "pending_approval", you can either skip or handle it differently
                    failed_assets.append(f"Asset {asset.serial_number} cannot be rejected due to its current status: {asset.status}.")

            # If there are no failed assets, trigger the background task
            if not failed_assets:
                # Trigger the background task to handle cart and asset cleanup after rejection
                # Correct call to background task
                process_rejected_cart_items() 
                
                return JsonResponse(
                    {"detail": "All assets in the checkout have been rejected and processed."},
                    status=status.HTTP_200_OK
                )

            # If there are failed assets, return a message with all the failed ones
            return JsonResponse(
                {"detail": "Some assets could not be rejected.", "failed_assets": failed_assets},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Checkout.DoesNotExist:
            return JsonResponse({"detail": "Checkout not found."}, status=status.HTTP_404_NOT_FOUND)



class CheckoutUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     # Ensure the user can only update their own checkouts
    #     return Checkout.objects.filter(user=self.request.user)
    
    
    
from django.http import HttpResponseNotFound
from django.shortcuts import render

def custom_404(request, exception=None):
    return render(request, 'qyfy/404.html', status=404)


def custom_505(request, exception=None):
    return render(request, 'qyfy/505.html', status=404)



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('home')  # Redirect to the home page after login
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')




def home_view(request):
    checkouts = Checkout.objects.all()  # Retrieve all checkout records
    return render(request, 'home.html', {
        'user': request.user,
        'checkouts': checkouts  # Pass checkouts to the template
    })



from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('login-form')  # Redirect to the login page or home page


def kenet_release_form_view(request):
    # You can add context data if needed, for example:
    context = {
        'logo_url': '/static/assets/images/logo.png',
        'stamp_url': '/static/assets/images/kenet_stamp.png'
        }
    return render(request, 'kenet_release_form.html', context)
    
    # If no additional context is needed, just render the template
    # return render(request, 'kenet_release_form.html')