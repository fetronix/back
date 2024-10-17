from rest_framework import serializers
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']


class AssetsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Serialize category details
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())

    class Meta:
        model = Assets
        fields = [
            'id',
            'date_received',
            'person_receiving',
            'asset_description',
            'serial_number',
            'kenet_tag',
            'location',  # Primary location
            'status',
            'category',
        ]
        
    def create(self, validated_data):
        # Handle category data
        category_data = validated_data.pop('category')
        
        # Use get_or_create for category, but ensure to handle it correctly
        category, created = Category.objects.get_or_create(
            name=category_data['name'],  # Assuming the category has a 'name' field
            defaults=category_data        # Use defaults to set other fields if necessary
        )

        # Handle location data
        location = validated_data.pop('location')  # Here we use the primary key of the location

        # Create the asset with all validated data
        asset = Assets.objects.create(
            category=category,
            location=location,
            **validated_data
        )
        return asset

    def validate(self, attrs):
        """
        Override the validate method to include custom validation if needed.
        """
        # Example validation (you can customize this)
        if 'serial_number' not in attrs or not attrs['serial_number']:
            raise serializers.ValidationError({"serial_number": "This field is required."})
        
        return attrs
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'supplier_name', 'quantity', 'person_receiving','invoice_file', 'invoice_number', 'project', 'comments']
        
        
class ViewAssetsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Serialize category details
    location = LocationSerializer()  # Serialize full location details
    new_location = LocationSerializer()  # Serialize full new location details

    class Meta:
        model = Assets
        fields = [
            'id',
            'date_received',
            'person_receiving',
            'asset_description',
            'serial_number',
            'kenet_tag',
            'location',  # Full location details
            'new_location',  # Full new location details
            'status',
            'category',
        ]
    
    def create(self, validated_data):
        # Handle category data
        category_data = validated_data.pop('category')
        category, created = Category.objects.get_or_create(**category_data)

        # Handle location data
        location_data = validated_data.pop('location')
        location, created = Location.objects.get_or_create(**location_data)

        # Handle new location data
        new_location_data = validated_data.pop('new_location')
        new_location, created = Location.objects.get_or_create(**new_location_data)

        # Create the asset with all validated data
        asset = Assets.objects.create(
            category=category,
            location=location,
            new_location=new_location,
            **validated_data
        )
        return asset


# serializers.py
from rest_framework import serializers
from .models import Assets

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = ['id', 'new_location', 'status']  # Include the fields you want to update



# serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from .models import CustomUser  # Adjust the import if necessary

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError('Invalid credentials, try again.')

        attrs['user'] = user
        return attrs


class CartSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)  # Nested asset details

    class Meta:
        model = Cart
        fields = ['id', 'asset', 'added_on']
        


# Add an asset to the cart
@api_view(['POST'])
def add_to_cart(request, asset_id):
    try:
        asset = Assets.objects.get(id=asset_id)
    except Assets.DoesNotExist:
        return Response({'error': 'Asset not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the asset is already in the cart
    if Cart.objects.filter(asset=asset).exists():
        return Response({'error': 'This asset is already in the cart.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the asset's status is 'instore'
    if asset.status != 'instore':
        return Response({'error': 'Only assets with "In Store" status can be added.'}, status=status.HTTP_400_BAD_REQUEST)

    # Add the asset to the cart
    Cart.objects.create(asset=asset)

    # Update the asset's status to 'pending_release'
    asset.status = 'pending_release'
    asset.save()

    return Response({'message': 'Asset added to cart and status updated to "pending_release".'})

# View all items in the cart
@api_view(['GET'])
def cart_view(request):
    cart_items = Cart.objects.all()
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)