# yourapp/decorators.py

from functools import wraps
from rest_framework import status
from apps.users.models import User
from core.response_handler.handler import ResponseHandler  # Import the ResponseHandler
from utils.messages import *

def check_user_info(func):
    """Decorator to check the status of the user before performing login or other actions."""
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        # Extract the email from the request data (assumes login is via email)
        email = request.data.get('email') or request.user.email

        if not email:
            return ResponseHandler.failure(
                message=EMAIL_FOUND_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Get user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return ResponseHandler.failure(
                message=USER_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND
            )
         # Check if the user is a staff or superuser
        if user.is_staff or user.is_superuser:
            return ResponseHandler.failure(
                message=ACCOUT_ACCESS_FOR_USER,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        # Check if the user is active
        if not user.is_active:
            return ResponseHandler.failure(
                message=ACCOUT_BLOCKED,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if the user is verified (assuming there's an 'is_verified' field)
        if not hasattr(user, 'is_verified') or not user.is_verified:
            return ResponseHandler.failure(
                message=EMAIL_NOT_VERIFIED,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # If all checks pass, call the original function
        return func(self, request, *args, **kwargs)

    return wrapper
