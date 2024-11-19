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
from django.views.generic import DetailView
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



from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def create_or_update_location(request):
    location_name = request.data.get('location_name', None)
    location_alias = request.data.get('location_alias', None)

    if not location_name or not location_alias:
        return Response({"detail": "Location name and alias are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the location already exists
    location, created = Location.objects.get_or_create(
        name=location_name, 
        name_alias=location_alias
    )

    # Return appropriate response based on whether the location was created or updated
    if created:
        return Response(LocationSerializer(location).data, status=status.HTTP_201_CREATED)
    else:
        return Response(LocationSerializer(location).data, status=status.HTTP_200_OK)

class AssetsCreateView(generics.CreateAPIView):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Handle location in assets creation
        location_data = request.data.get('location', None)

        if location_data:
            location_name = location_data.get('name', None)
            location_alias = location_data.get('name_alias', None)

            if location_name and location_alias:
                location, created = Location.objects.get_or_create(name=location_name, name_alias=location_alias)
                # Assign the created or existing location to the asset
                request.data['location'] = location.id

        return super().create(request, *args, **kwargs)

# class AssetsCreateView(generics.CreateAPIView):
#     queryset = Assets.objects.all()
#     serializer_class = AssetsSerializer
#     permission_classes = [permissions.IsAuthenticated]  # Ensure authentication
    
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

class UserCheckoutSet(viewsets.ModelViewSet):
    serializer_class = CustomUserCheckoutSerializer

    def get_queryset(self):
        """
        Exclude the logged-in user and optionally filter by role.
        """
        # Get the logged-in user
        logged_in_user = self.request.user

        # Get role parameter from query parameters
        role = self.request.query_params.get('role', None)

        # Base queryset: exclude the logged-in user
        queryset = CustomUser.objects.exclude(id=logged_in_user.id)

        if role:
            # Filter by role if provided
            return queryset.filter(role=role)

        # Default to returning users with 'can_checkout_items' role
        return queryset.filter(role=UserRoles.CAN_VERIFY_ITEMS)

    
class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    

    def get_queryset(self):
        user = self.request.user
        
        # Optionally, you can call the task here if needed, e.g., for real-time expiration check
        remove_expired_cart_items(schedule=10)
        
        return Cart.objects.filter(user=user, asset__status='pending_release')
    
    



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Cart, Assets
from background_task.models import Task
from .tasks import remove_expired_cart_items

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

        # Schedule the background task to remove expired cart items
        # remove_expired_cart_items()  # You can specify the delay as needed

        return Response({'message': 'Added to cart'}, status=status.HTTP_201_CREATED)



class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def delete(self, request, asset_id):
        user = request.user
        cart_item = get_object_or_404(Cart, id=asset_id)
        
        if cart_item:
            # Get the asset related to the cart item
            asset = get_object_or_404(Assets, id=cart_item.asset.id)  # Assuming Cart has a foreign key to Asset

            # Update the asset status to 'instore'
            asset.status = 'instore'
            asset.save()

            # Remove the item from the cart
            cart_item.delete()
            return Response({'message': 'Removed from Dispatch basket'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Item not in Dispatch basket'}, status=status.HTTP_400_BAD_REQUEST)



class CheckoutCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        verified_user = request.data.get('verified_user')
        print("-----------------------------------------------")
        
        print(verified_user)
        
        print("-----------------------------------------------")
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
        
        v_user = CustomUser.objects.get(username=verified_user)
        
        checkout.verifier_user = CustomUser.objects.get(username=verified_user)
        
        checkout.save()

        # Update the status and location of the assets in the cart
        for cart_item in cart_items:
            asset = cart_item.asset
            asset.status = 'pending_approval'  # Update the status
            asset.going_location = new_location  # Set the new location
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
    serializer_class = CheckoutSerializer

    def get_queryset(self):
        # Get the logged-in user
        logged_in_user = self.request.user

        # Retrieve the first name and last name of the logged-in user
        user_first_name = logged_in_user.first_name
        user_last_name = logged_in_user.last_name
        username = logged_in_user.username
        usernameid = logged_in_user.id

        # Filter checkouts where the verifier_user matches the logged-in user's first or last name
        queryset = Checkout.objects.filter(
            models.Q(verifier_user=usernameid) | models.Q(verifier_user=usernameid)
        )

        if queryset.exists():
            return queryset
        else:
            # If no matching checkouts exist, return an empty queryset
            return Checkout.objects.none()

class CheckoutDetailView(DetailView):
    model = Checkout
    template_name = 'kenet_release_form.html'  # Create this template for displaying the details
    context_object_name = 'checkout'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo_url'] = '/static/assets/images/logo.png'  # Adding logo URL
        context['stamp_url'] = '/static/assets/images/kenet_stamp.png'  # Adding stamp URL
        return context

    
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Checkout

class ApproveCheckoutView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, checkout_id, *args, **kwargs):
        try:
            checkout = Checkout.objects.get(id=checkout_id)
            cart_items = checkout.cart_items.all()

            failed_assets = []
            for cart_item in cart_items:
                asset = cart_item.asset
                if asset.status == 'approved':
                    failed_assets.append(f"Asset {asset.serial_number} is already approved.")
                elif asset.status == 'pending_approval':
                    asset.status = 'approved'
                    asset.save()
                else:
                    failed_assets.append(f"Asset {asset.serial_number} cannot be approved due to its current status: {asset.status}.")

            if not failed_assets:
                # Generate the checkout detail URL link
                checkout_url = request.build_absolute_uri(reverse('checkout-detail', args=[checkout_id]))

                # Save the generated URL in the `checkout_url_link` field
                checkout.checkout_url_link = checkout_url
                checkout.save()

                # save_approved_asset_movements()

                return Response(
                    {
                        "detail": "All assets in the checkout have been approved.",
                        "checkout_url_link": checkout_url
                    },
                    status=status.HTTP_200_OK
                )

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

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone

class CheckoutUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Save the updated checkout instance
        checkout = serializer.save()
        
        # Iterate through each cart item linked to this checkout
        for cart_item in checkout.cart_items.all():
            asset = cart_item.asset
            
            # Create an AssetsMovement entry for each asset in the checkout cart
            AssetsMovement.objects.create(
                assets=asset,
                date_created=timezone.now(),
                person_moving=self.request.user,
                comments=checkout.remarks,
                serial_number=asset.serial_number,
                asset_description = asset.asset_description,
                asset_description_model = asset.asset_description_model,
                kenet_tag=asset.kenet_tag,
                status="onsite",  # Set the movement record status to "onsite"
                location=asset.location.name if asset.location else None,
                new_location=asset.going_location,
            )

            # Update the asset status to "onsite"
            asset.status = "onsite"
            asset.save()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        
        # Customize the response if needed
        response.data['message'] = "Checkout updated, asset status set to onsite, and movements recorded"
        return Response(response.data, status=status.HTTP_200_OK)

class CheckoutUSerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutUserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

   
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        
        # Customize the response if needed
        response.data['message'] = "Checkout updated, asset status set to onsite, and movements recorded"
        return Response(response.data, status=status.HTTP_200_OK)

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
    assets = Assets.objects.all()  # Retrieve all checkout records
    return render(request, 'home.html', {
        'user': request.user,
        'assets': assets  # Pass checkouts to the template
    })
    

import requests
from requests.auth import HTTPBasicAuth
from django.shortcuts import render
from django.http import JsonResponse
from .models import Assets

# Define the view that handles the SOAP request
def create_fixed_asset(request, asset_id):
    try:
        # Fetch the asset using the provided asset_id
        asset = Assets.objects.get(id=asset_id)

        # Prepare asset data (you can add more fields as per your requirements)
        asset_data = {
            'Description': asset.asset_description,
            'FA_Class_Code': 'TANGIBLE',  # This might come from another model or hardcoded
            'FA_Subclass_Code': 'NET-EQUIP',  # Similarly, this can be dynamic
            'Tag_Number': asset.kenet_tag,
            'Serial_No': asset.serial_number,
        }

        # SOAP request body (replace with dynamic fields as required)
        soap_body = f"""
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
                <Create xmlns="urn:microsoft-dynamics-schemas/page/fixedassetcard">
                    <FixedAssetCard>
                        <Description>{asset_data['Description']}</Description>
                        <FA_Class_Code>{asset_data['FA_Class_Code']}</FA_Class_Code>
                        <FA_Subclass_Code>{asset_data['FA_Subclass_Code']}</FA_Subclass_Code>
                        <Tag_Number>{asset_data['Tag_Number']}</Tag_Number>
                        <Serial_No>{asset_data['Serial_No']}</Serial_No>
                    </FixedAssetCard>
                </Create>
            </s:Body>
        </s:Envelope>
        """

        # Define the SOAP endpoint and authentication details
        soap_url = "http://a01-test.erp.kenet.or.ke:7047/BC190/WS/KENET%20LIVE/Page/FixedAssetCard"
        username = 'GLUORA'
        password = 'GOL@#k3n3t?!!'


        # SOAP headers
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "urn:microsoft-dynamics-schemas/page/fixedassetcard:Create"
        }

        # Send the SOAP request
        response = requests.post(
            soap_url,
            data=soap_body,
            headers=headers,
            auth=HTTPBasicAuth(username, password)
        )

        # Check the response status
        if response.status_code == 200:
            asset.sent_to_erp = True
            asset.save()
             # Add a success message
            messages.success(request, f"Fixed asset with Serial Number {asset.serial_number} sent successfully in ERP.")
            return redirect('http://197.136.16.164:8000/admin/KENETAssets/assets/')
        
        
        else:
            messages.error(request, f"Failed to send fixed asset in ERP. Error: {response.text}")
            return redirect('http://197.136.16.164:8000/admin/KENETAssets/assets/')

    except Assets.DoesNotExist:
        messages.error(request, f"Asset with Serial Number {asset.serial_number} not found.")
        return redirect('http://197.136.16.164:8000/admin/KENETAssets/assets/')
    except Exception as e:
        messages.error(request, f"An error occurred while updating asset: {str(e)}")
        return redirect('http://197.136.16.164:8000/admin/KENETAssets/assets/')


# Define the view that handles the SOAP request
def update_fixed_asset(request, asset_id):
    try:
        # Fetch the asset using the provided asset_id
        asset = AssetsMovement.objects.get(id=asset_id)
        
        
        print(asset)

        # Prepare asset data (you can add more fields as per your requirements)
        asset_data = {
            'Description': asset.asset_description,
            'FA_Class_Code': 'TANGIBLE',  # This might come from another model or hardcoded
            'FA_Subclass_Code': 'NET-EQUIP',  # Similarly, this can be dynamic
            'Tag_Number': asset.kenet_tag,
            'Serial_No': asset.serial_number,
        }

        # SOAP request body (replace with dynamic fields as required)
        soap_body = f"""
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
                <Create xmlns="urn:microsoft-dynamics-schemas/page/fixedassetcard">
                    <FixedAssetCard>
                        <Description>{asset_data['Description']}</Description>
                        <FA_Class_Code>{asset_data['FA_Class_Code']}</FA_Class_Code>
                        <FA_Subclass_Code>{asset_data['FA_Subclass_Code']}</FA_Subclass_Code>
                        <Tag_Number>{asset_data['Tag_Number']}</Tag_Number>
                        <Serial_No>{asset_data['Serial_No']}</Serial_No>
                        <FA_Location_Code>AGHAKAN-UN</FA_Location_Code>
                    </FixedAssetCard>
                </Create>
            </s:Body>
        </s:Envelope>
        """

        # Define the SOAP endpoint and authentication details
        soap_url = "http://a01-test.erp.kenet.or.ke:7047/BC190/WS/KENET%20LIVE/Page/FixedAssetCard"
        username = 'GLUORA'
        password = 'GOL@#k3n3t?!!'


        # SOAP headers
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "urn:microsoft-dynamics-schemas/page/fixedassetcard:Update"
        }

        # Send the SOAP request
        response = requests.post(
            soap_url,
            data=soap_body,
            headers=headers,
            auth=HTTPBasicAuth(username, password)
        )

        # Check the response status
        if response.status_code == 200:
            asset.sent_to_erp = True
            asset.save()
            
            messages.success(request, f"Fixed asset with Serial Number {asset.serial_number} updated successfully in ERP.")
            return redirect('http://197.136.16.164:8000/admin/KENETAssets/assetsmovement/')
        
        
        else:
            messages.error(request, f"Failed to update fixed asset in ERP. Error: {response.text}")
            return redirect('http://197.136.16.164:8000/admin/KENETAssets/assetsmovement/')

    except Assets.DoesNotExist:
        messages.error(request, f"Asset with Serial Number {asset.serial_number} not found.")
        return redirect('http://197.136.16.164:8000/admin/KENETAssets/assetsmovement/')
    except Exception as e:
        messages.error(request, f"An error occurred while updating asset: {str(e)}")
        return redirect('http://197.136.16.164:8000/admin/KENETAssets/assetsmovement/')


from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('login-form')  # Redirect to the login page or home page


import logging

logger = logging.getLogger(__name__)


def kenet_release_form_view(request):
    # Example checkout object, replace with your logic to get the correct checkout
    checkout = get_object_or_404(Checkout, id=request.GET.get("id")) 

    # Initialize the variables in case the user is not found
    authorizing_first_name = "Unknown"
    authorizing_last_name = "User"

    authorizing_user = CustomUser.objects.get(username=checkout.authorizing_name)
    authorizing_first_name = authorizing_user.first_name
    authorizing_last_name = authorizing_user.last_name

    # Add to context
    context = {
        'checkout': checkout,
        'logo_url': '/static/assets/images/logo.png',
        'stamp_url': '/static/assets/images/kenet_stamp.png',
        'authorizing_first_name': authorizing_first_name,
        'authorizing_last_name': authorizing_last_name,
    }
    return render(request, 'kenet_release_form.html', context)

    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Assets, Cart, Checkout
class ReturnFaultyAssetView(APIView):
    allowed_methods = ['GET', 'POST', 'PATCH']  # Allow PATCH as well
    
    def get(self, request, asset_id, *args, **kwargs):
        # Fetch and return asset details for GET requests
        asset = get_object_or_404(Assets, id=asset_id)
        # Assuming you have a serializer to return the asset data
        # serializer = AssetSerializer(asset)
        return Response({"asset_id": asset.id, "status": asset.status}, status=status.HTTP_200_OK)
    
    def post(self, request, asset_id, *args, **kwargs):
        # Mark the asset as faulty and remove it from cart/checkout
        return self.handle_faulty_asset(request, asset_id)
    
    def patch(self, request, asset_id, *args, **kwargs):
        # Handle partial updates (you can mark as faulty and remove from cart)
        return self.handle_faulty_asset(request, asset_id)
    
    def handle_faulty_asset(self, request, asset_id):
        try:
            # Get the asset by ID
            asset = get_object_or_404(Assets, id=asset_id)

            # Check if the asset's status is already 'faulty'
            if asset.status == 'faulty':
                return Response(
                    {"detail": "Asset is already marked as faulty."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Mark asset status as 'faulty'
            asset.status = 'faulty'

            # Check if the asset exists in any checkout or cart
            cart_item = Cart.objects.filter(asset=asset).first()
            checkout = Checkout.objects.filter(cart_items__asset=asset).first()

            with transaction.atomic():
                if checkout:
                    # Remove the asset from the checkout
                    checkout.cart_items.remove(cart_item)
                    checkout.save()

                if cart_item:
                    # Delete the cart item (if not deleted above)
                    cart_item.delete()

                # Revert `new_location` to null
                asset.new_location = "UON Store"
                asset.save()

            return Response(
                {"detail": "Asset has been marked as faulty and removed from any checkouts or carts."},
                status=status.HTTP_200_OK
            )

        except Assets.DoesNotExist:
            return Response({"detail": "Asset not found."}, status=status.HTTP_404_NOT_FOUND)

class ReturnDecomissionedAssetView(APIView):
    allowed_methods = ['GET', 'POST', 'PATCH']  # Allow PATCH as well
    
    def get(self, request, asset_id, *args, **kwargs):
        # Fetch and return asset details for GET requests
        asset = get_object_or_404(Assets, id=asset_id)
        # Assuming you have a serializer to return the asset data
        # serializer = AssetSerializer(asset)
        return Response({"asset_id": asset.id, "status": asset.status}, status=status.HTTP_200_OK)
    
    def post(self, request, asset_id, *args, **kwargs):
        # Mark the asset as faulty and remove it from cart/checkout
        return self.handle_faulty_asset(request, asset_id)
    
    def patch(self, request, asset_id, *args, **kwargs):
        # Handle partial updates (you can mark as faulty and remove from cart)
        return self.handle_faulty_asset(request, asset_id)
    
    def handle_faulty_asset(self, request, asset_id):
        try:
            # Get the asset by ID
            asset = get_object_or_404(Assets, id=asset_id)

            # Check if the asset's status is already 'faulty'
            if asset.status == 'decommissioned':
                return Response(
                    {"detail": "Asset is already marked as decommissioned."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Mark asset status as 'faulty'
            asset.status = 'decommissioned'

            # Check if the asset exists in any checkout or cart
            cart_item = Cart.objects.filter(asset=asset).first()
            checkout = Checkout.objects.filter(cart_items__asset=asset).first()

            with transaction.atomic():
                if checkout:
                    # Remove the asset from the checkout
                    checkout.cart_items.remove(cart_item)
                    checkout.save()

                if cart_item:
                    # Delete the cart item (if not deleted above)
                    cart_item.delete()

                # Revert `new_location` to null
                asset.new_location = "UON Store"
                asset.save()

            return Response(
                {"detail": "Asset has been marked as decommissioned and removed from any checkouts or carts."},
                status=status.HTTP_200_OK
            )

        except Assets.DoesNotExist:
            return Response({"detail": "Asset not found."}, status=status.HTTP_404_NOT_FOUND)
