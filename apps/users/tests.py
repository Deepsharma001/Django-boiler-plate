# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework.test import APITestCase
# from rest_framework import status
# from unittest.mock import patch
# # from app.views import AuthSignupViewSet  # Replace 'app' with the actual app name
# from django.contrib.auth.models import Group
# from apps.users.models import User

# # Test case class
# class AuthSignupViewSetTest(APITestCase):
    
#     @classmethod
#     def setUpTestData(cls):
#         cls.signup_url = '/api/auth/register/'  # URL for the endpoint
    
#     def setUp(self):
#         self.valid_data = {
#             "email": "testuser@example.com",
#             "password": "Test@1234?",
#             "first_name": "Test",
#             "last_name": "User"
#         }

#     @patch('apps.users.authentications.signup.views.AuthSignupViewSet.send_verification_email')
#     def test_create_user_success(self, mock_send_verification_email):
#         """Test successful creation of a new user."""
#         response = self.client.post(self.signup_url, data=self.valid_data)
        
#         print(response.data)  # Add this line to see the error message
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["message"], "Account successfully created. A verification link has been sent to your email.")
#         self.assertTrue(User.objects.filter(email=self.valid_data["email"]).exists())
#         mock_send_verification_email.assert_called_once()

#     def test_create_user_existing_email(self):
#         """Test failure when creating a user with an existing email."""
#         # Create the first user
#         User.objects.create_user(email=self.valid_data["email"], password="Password123")

#         # Try to create a new user with the same email
#         response = self.client.post(self.signup_url, data=self.valid_data)
        
#         # Assert that the response has the expected failure status and message
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data["message"], "User already exists!")

#     def test_create_user_invalid_email(self):
#         """Test failure when the provided email is invalid."""
#         # Use invalid email
#         invalid_email_data = {
#             "email": "invalid-email",  # Invalid email format
#             "password": "StrongPassword123",
#             "first_name": "Test",
#             "last_name": "User"
#         }
        
#         # Send the request
#         response = self.client.post(self.signup_url, data=invalid_email_data)
        
#         # Assert failure due to invalid email
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("Please enter a valid email address.", response.data["message"])

#     def test_atomicity_on_failure(self):
#         """Test that no user is created if an error occurs during the signup process."""
#         # Patch the create_user method to raise an exception during the creation process
#         with patch('apps.users.authentications.signup.views.AuthSignupViewSet.create_user', side_effect=Exception("Unexpected error")):
#             # Send the request
#             response = self.client.post(self.signup_url, data=self.valid_data)
            
#             # Assert the failure status code
#             self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
#             # Assert that no user was created
#             self.assertFalse(User.objects.filter(email=self.valid_data["email"]).exists())
            
from django.urls import path, include
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from apps.users.models import User
from rest_framework.authtoken.models import Token
from utils.messages import USER_LOGGED_IN, INVALID_USER_CREDENTIAL

class AuthLoginViewSetTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.login_url = '/api/auth/login/'  # URL for the endpoint
    
    def setUp(self):
        self.valid_user_data = {
            'email': 'testuser@example.com',
            'password': 'Test@1234?'
        }
        self.invalid_user_data = {
            'email': 'testuser@example.com',
            'password': 'WrongPassword'
        }
        self.non_existent_user_data = {
            'email': 'nonexistent@example.com',
            'password': 'Test@1234?'
        }
        # Create a user
        self.user = User.objects.create_user(
            email=self.valid_user_data['email'],
            password=self.valid_user_data['password'],
            first_name="Test",
            last_name="User"
        )
    
    @patch('core.baseviewset.authentication.token_expire_handler')
    def test_login_success(self, mock_token_expire_handler):
        """Test successful login with valid credentials."""
        response = self.client.post(self.login_url, data=self.valid_user_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], USER_LOGGED_IN)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('user_type', response.data)

    # def test_login_invalid_password(self):
    #     """Test failure when an invalid password is provided."""
    #     response = self.client.post(self.login_url, data=self.invalid_user_data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['message'], INVALID_USER_CREDENTIAL)

    # def test_login_non_existent_user(self):
    #     """Test failure when the email does not exist."""
    #     response = self.client.post(self.login_url, data=self.non_existent_user_data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['message'], INVALID_USER_CREDENTIAL)
    
    # @patch('core.baseviewset.authentication.token_expire_handler')
    # def test_login_with_expired_token(self, mock_token_expire_handler):
    #     """Test expired token handling during login."""
    #     mock_token_expire_handler.return_value = (True, None)  # Simulate expired token
    #     response = self.client.post(self.login_url, data=self.valid_user_data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], USER_LOGGED_IN)
    #     self.assertIn('token', response.data)
