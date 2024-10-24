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
from .serializers import *  # Assuming you've already created a LoginSerializer
from django.shortcuts import get_object_or_404


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
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    


# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, Assets
from .serializers import CartSerializer, CartDetailSerializer

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


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ReleaseFormData  # Assuming you have a model to save form data

def release_form(request):
    if request.method == "POST":
        # Extract data from the form
        name = request.POST.get('name')
        date = request.POST.get('date')
        current_location = request.POST.get('current_location')
        new_location = request.POST.get('new_location')
        description = request.POST.get('description')
        quantity_required = request.POST.get('quantity_required')
        quantity_issued = request.POST.get('quantity_issued')
        serial_number = request.POST.get('serial_number')
        kenet_tag = request.POST.get('kenet_tag')
        authorizing_name = request.POST.get('authorizing_name')
        authorization_date = request.POST.get('authorization_date')

        # Save the data to the database (you should define the ReleaseFormData model accordingly)
        release_form_data = ReleaseFormData(
            name=name,
            date=date,
            current_location=current_location,
            new_location=new_location,
            description=description,
            quantity_required=quantity_required,
            quantity_issued=quantity_issued,
            serial_number=serial_number,
            kenet_tag=kenet_tag,
            authorizing_name=authorizing_name,
            authorization_date=authorization_date,
        )
        release_form_data.save()

        # Redirect to a success page (or render the same page with a success message)
        return redirect('success')  # Define a success URL or page

    return render(request, 'qyfy/release_form.html')
