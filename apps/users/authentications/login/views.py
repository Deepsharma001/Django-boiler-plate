from django.http import HttpResponse
from rest_framework import status
from django.utils import timezone
from apps.users.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from core.baseviewset.authentication import token_expire_handler
from core.baseviewset.viewset import aBaseViewset, nBaseViewset
from apps.users.authentications.login.serializers import UserLoginSerializer
from core.decorators.check_user_info import check_user_info
from drf_yasg.utils import swagger_auto_schema
from core.response_handler.handler import ResponseHandler
from rest_framework.serializers import Serializer  
from utils.messages import *

def home(request):
    data = "<h1>Welcome to Django</h1>"
    return HttpResponse(data)

class AuthLoginViewSet(nBaseViewset):
    queryset = User.objects
    serializer_class = UserLoginSerializer
    http_method_names = ['post']
    
    @swagger_auto_schema(
        operation_description="allow the user to login",
        request_body=UserLoginSerializer,
        responses={
            status.HTTP_200_OK: USER_LOGGED_IN,
            status.HTTP_400_BAD_REQUEST: HTTP_400_BAD_REQUEST,
            status.HTTP_500_INTERNAL_SERVER_ERROR: HTTP_500_INTERNAL_SERVER_ERROR
        },
        tags=['User Authentication']
    ) 
    @check_user_info
    def create(self, request, *args, **kwargs):
        """Handle user login and return authentication token."""
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            user = User.objects.get(email=email)

            if not user.check_password(password):
                raise ValueError(INVALID_USER_CREDENTIAL)
            
            token, created = Token.objects.get_or_create(user=user)
            is_expired, token = token_expire_handler(token)
            
            # Update user last login time
            user.last_login = timezone.now()
            user.save()

            return ResponseHandler.success(
                message=USER_LOGGED_IN,
                data={
                    "token": token.key,
                    "user_type": user.user_type,
                    "user_id": user.id,
                    "photo": user.profile_photo.url if user.profile_photo else None,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            )
        
        except Exception as error:
            return ResponseHandler.failure(
                message=str(error),
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
class AuthLogoutViewSet(aBaseViewset):
    """Viewset to handle user logout and related operations."""
    queryset = User.objects.all()
    serializer_class = Serializer  # Pass blank serializer since no data is required for logout
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Logs out the user and clears any device-specific data.",
        request_body=None,  # No body expected for logout
        responses={
            status.HTTP_200_OK: USER_LOGGED_OUT,
            status.HTTP_400_BAD_REQUEST: HTTP_400_BAD_REQUEST
        },
        tags=['User Authentication']

    )
    def create(self, request, *args, **kwargs):
        """Log out the user and clear any device-specific data."""
        try:
            user = request.user
            # Delete existing tokens
            Token.objects.filter(user=user).delete()
            # Perform logout
            logout(request)

            # Return success response
            return ResponseHandler.success(
                message=USER_LOGGED_OUT,
                status_code=status.HTTP_200_OK
            )

        except Exception as error:
            # Handle errors and return failure response
            return ResponseHandler.failure(
                message=str(error),
                status_code=status.HTTP_400_BAD_REQUEST
            )
