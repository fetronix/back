from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *

class AssetsListCreate(generics.ListCreateAPIView):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class LocationListCreate(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

from django.shortcuts import render
from rest_framework import generics
from .models import Assets
from .serializers import AssetsSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class AssetCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AssetsSerializer(data=request.data)
        if serializer.is_valid():
            asset = serializer.save()
            return Response(AssetsSerializer(asset).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssetsViewListCreate(generics.ListCreateAPIView):
    queryset = Assets.objects.all()
    serializer_class = ViewAssetsSerializer

import openpyxl
from django.http import HttpResponse
from rest_framework import generics
from .models import Assets
from .serializers import AssetsSerializer

class AssetsExportView(generics.ListAPIView):
    queryset = Assets.objects.all()  # Set the queryset here
    serializer_class = AssetsSerializer

    def get(self, request, *args, **kwargs):
        # Create a workbook and add a worksheet
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = 'Assets'

        # Define the headers
        headers = ['Date Received', 'Person Receiving', 'Asset Description', 'Serial Number', 'KENET Tag', 'Location']
        worksheet.append(headers)

        # Fetch assets using get_queryset() and write to the worksheet
        for asset in self.get_queryset():  # Use get_queryset() instead of accessing self.queryset
            worksheet.append([
                asset.date_received,
                asset.person_receiving,
                asset.asset_description,
                asset.serial_number,
                asset.kenet_tag,
                asset.location,
            ])

        # Create HTTP response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=assets.xlsx'
        
        # Save the workbook to the response
        workbook.save(response)
        return response



from django.shortcuts import render
from .models import Assets

def assets_list(request):
    assets = Assets.objects.all()
    return render(request, 'qyfy/assets_list.html', {'assets': assets})




class DeliveryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    
    
# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Assets
from .serializers import AssetSerializer

class AssetUpdateView(APIView):
    def put(self, request, pk, format=None):
        try:
            asset = Assets.objects.get(pk=pk)
        except Assets.DoesNotExist:
            return Response({'error': 'Asset not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AssetSerializer(asset, data=request.data, partial=True)  # partial=True allows updating only the provided fields
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# views.py

from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import LoginSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Log the user in (this will create a session for the user)
        login(request, user)

        # Return a response indicating that the login was successful
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
            },
            'message': 'Login successful.',
        }, status=status.HTTP_200_OK)
