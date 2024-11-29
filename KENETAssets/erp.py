from .models import *
from .serializers import *  
from django.contrib import messages
from django.shortcuts import  redirect
import requests
from requests.auth import HTTPBasicAuth




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

