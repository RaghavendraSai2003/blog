import os
import django
import jwt
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_site.settings")
django.setup()

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from blog.auth_views import MyTokenObtainPairView

# Create a test user
username = 'jwt_test_user'
password = 'testpassword123'
email = 'jwt@test.com'

try:
    user = User.objects.get(username=username)
    user.delete()
except User.DoesNotExist:
    pass

user = User.objects.create_user(username=username, email=email, password=password)

# Make request to obtain token WITHOUT password
factory = APIRequestFactory()
# NOTE: Only username and email should be required now
request = factory.post('/api/token/', {'username': username, 'email': email}, format='json')
view = MyTokenObtainPairView.as_view()
response = view(request)

if response.status_code == 200:
    access_token = response.data['access']
    print(f"Access Token: {access_token[:20]}...")
    
    # Decode token
    payload = jwt.decode(access_token, options={"verify_signature": False})
    
    print("Payload Keys:", payload.keys())
    
    if 'username' in payload and payload['username'] == username:
        print("PASS: Username is in payload.")
    else:
        print("FAIL: Username missing or incorrect.")

    if 'email' in payload and payload['email'] == email:
        print("PASS: Email is in payload.")
    else:
        print("FAIL: Email missing or incorrect.")
        
    print("PASS: Token obtained without password.")

else:
    print(f"FAIL: Could not obtain token. Status: {response.status_code}")
    print(response.data)
