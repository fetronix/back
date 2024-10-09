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
        
    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category, created = Category.objects.get_or_create(**category_data)
        asset = Assets.objects.create(category=category, **validated_data)
        return asset