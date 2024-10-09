from rest_framework import serializers
from .models import Assets, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AssetsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Serialize category details

    class Meta:
        model = Assets
        fields = [
            'asset_description', 'category', 'person_receiving', 
            'serial_number', 'kenet_tag', 'location', 'status', 
            'date_received', 'new_location'
        ]
