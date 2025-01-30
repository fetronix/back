import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the values
soap_url = os.getenv('SOAP_URL')
username = os.getenv('ERP_USERNAME')
password = os.getenv('ERP_PASSWORD')

# Print the values
print(f"SOAP_URL: {soap_url}")
print(f"ERP_USERNAME: {username}")
print(f"ERP_PASSWORD: {password}")
