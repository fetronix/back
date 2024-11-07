from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # You can specify specific fields if needed

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'  # You can specify specific fields if needed

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'  # You can specify specific fields if needed


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name','last_name']

class AssetsSerializer(serializers.ModelSerializer):
    
    person_receiving = serializers.StringRelatedField()  # Use this if you have a __str__ method in the PersonReceiving model
    location = LocationSerializer()  # Nested serializer
    category = CategorySerializer()  # Nested serializer
    class Meta:
        model = Assets
        fields = [
            'id', 
            'date_received', 
            'person_receiving', 
            'asset_description', 
            'new_location',
            'serial_number', 
            'kenet_tag', 
            'location',
            'status', 
            'category'
        ]
   
class DeliveryListSerializer(serializers.ModelSerializer):
    
    person_receiving = serializers.StringRelatedField()  # Use this if you have a __str__ method in the PersonReceiving model
    supplier_name = serializers.StringRelatedField()
    class Meta:
        model = Delivery
        fields = [
             'id',
            'person_receiving',
            'date_delivered',
            'supplier_name',
            'quantity',
            'invoice_file',
            'invoice_number',  
            'project',
            'comments',
            'delivery_id',
        ]
   
        


class AssetCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()) # Serialize category details
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    person_receiving = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    delivery = serializers.PrimaryKeyRelatedField(queryset=Delivery.objects.all())

    # We will auto-fill 'person_receiving' in the view, so no need for the queryset here
    # person_receiving = serializers.CharField(read_only=True)

    class Meta:
        model = Assets
        fields = [
            'id',
            'date_received',
            'person_receiving',
            'asset_description',
            'asset_description_model',
            'serial_number',
            'kenet_tag',
            'location',  # Primary location
            'status',
            'category',
            'delivery',
        ]
        
    def create(self, validated_data):
        category_data = validated_data.pop('category')
        location = validated_data.pop('location')
        person_receiving = validated_data.pop('person_receiving')
        delivery = validated_data.pop('delivery')

        # Create the asset with the remaining validated data
        asset = Assets.objects.create(
            category=category_data,
            location=location,
            person_receiving=person_receiving,
            delivery=delivery,
            **validated_data
        )
        return asset

    def validate(self, attrs):
        # Custom validation if necessary
        if 'serial_number' not in attrs or not attrs['serial_number']:
            raise serializers.ValidationError({"serial_number": "This field is required."})
        
        return attrs
    

class DeliveryCreateSerializer(serializers.ModelSerializer):
    person_receiving = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    supplier_name = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all())
    class Meta:
        model = Delivery
        fields = [
            'id',
            'date_delivered',
            'person_receiving',
            'supplier_name',
            'quantity',
            'invoice_file',
            'invoice_number', 
            'project',
            'comments',
        ]
        
    def create(self, validated_data):

        person_receiving = validated_data.pop('person_receiving')
        supplier_name = validated_data.pop('supplier_name')

        # Create the asset with the remaining validated data
        assets = Delivery.objects.create(
           
            person_receiving=person_receiving,
            supplier_name=supplier_name,
            **validated_data
        )
        return assets

    def validate(self, attrs):
        # Custom validation if necessary
        if 'invoice_number' not in attrs or not attrs['invoice_number']:
            raise serializers.ValidationError({"invoice_number": "This field is required."})
        
        return attrs
# serializers.py

from rest_framework import serializers
from .models import Cart, Assets

class CartSerializer(serializers.ModelSerializer):
    asset = serializers.StringRelatedField()  # You can use asset fields as needed
    user = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'asset', 'added_at']

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = ['status','new_location']

    def update(self, instance, validated_data):
        # Handle updating the new location and status
        instance.new_location = validated_data.get('new_location', instance.new_location)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class CartDetailSerializer(serializers.ModelSerializer):
    asset = serializers.StringRelatedField()  # Displaying asset as a string

    class Meta:
        model = Cart
        fields = ['id', 'user', 'asset', 'added_at']




from rest_framework import serializers
from .models import Checkout, Cart
from .serializers import CartSerializer

class CheckoutSerializer(serializers.ModelSerializer):
    cart_items = CartSerializer(many=True, read_only=True)

    class Meta:
        model = Checkout
        fields = ['id', 'user', 'cart_items', 'checkout_date', 'remarks']



class CheckoutUpdateSerializer(serializers.ModelSerializer):
    # Field to accept base64 signature data for updating the signature image
    signature_image = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Checkout
        fields = ['remarks', 'signature_image', 'quantity_required', 'quantity_issued', 'authorizing_name']
        extra_kwargs = {
            'quantity_required': {'required': False},
            'quantity_issued': {'required': False},
            'remarks': {'required': False},
            'authorizing_name': {'required': False},
        }

    def update(self, instance, validated_data):
        # Update remarks
        instance.remarks = validated_data.get('remarks', instance.remarks)

        # Update signature image if signature_base64 is provided
        signature_image = validated_data.get('signature_image')
        if signature_image:
            instance.save_signature(signature_image)

        # Update quantity fields
        instance.quantity_required = validated_data.get('quantity_required', instance.quantity_required)
        instance.quantity_issued = validated_data.get('quantity_issued', instance.quantity_issued)

        # Update authorizing name
        instance.authorizing_name = validated_data.get('authorizing_name', instance.authorizing_name)

        instance.save()
        return instance