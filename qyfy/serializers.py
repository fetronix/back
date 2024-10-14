from rest_framework import serializers
from .models import *

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
    new_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())

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
            'new_location',  # New location
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
    
    
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'supplier_name', 'quantity', 'person_receiving', 'invoice_file', 'invoice_number', 'project', 'comments']
        
        
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
