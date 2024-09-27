from rest_framework import serializers
from .models import Assets

class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = '__all__'  # Or specify fields as a list
