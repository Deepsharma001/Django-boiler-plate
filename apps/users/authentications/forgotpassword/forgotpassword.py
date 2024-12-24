import random
import threading
import requests
from rest_framework import viewsets, status
from apps.users.models import User
from core.baseviewset.viewset import nBaseViewset
from core.validators.email_password_validator import password_check
from utils.send_email import send_forgot_password_mail
from apps.users.authentications.forgotpassword.serializers import ChangePasswordSerializer, ForgotPasswordSerializer
from rest_framework.serializers import Serializer  
from core.response_handler.handler import ResponseHandler
from drf_yasg.utils import swagger_auto_schema
from core.response_handler.handler import ResponseHandler
from utils.messages import *

class ForgotPasswordViewSet(nBaseViewset):
    """Viewset to handle forgot password request and sending OTP."""
    queryset = User.objects
    serializer_class = ForgotPasswordSerializer
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Allows the user to reset their password by sending an OTP to their registered email.",
        request_body=ForgotPasswordSerializer,
        responses={
            status.HTTP_200_OK: OTP_SENT_SUCCESS,
            status.HTTP_400_BAD_REQUEST: EMAIL_FOUND_ERROR,
            status.HTTP_500_INTERNAL_SERVER_ERROR: HTTP_500_INTERNAL_SERVER_ERROR
        },
        tags=['User Authentication']
    )
    
    def create(self, request, *args, **kwargs):
        """Initiate password reset by sending OTP to the user's registered email."""
        try:
            email = request.data['email']
            
            # Check if user exists with provided email
            if not User.objects.filter(email=email).exists():
                return ResponseHandler.failure(
                    message=EMAIL_NOT_REGISTERED,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            # Get the user object
            user = User.objects.get(email=email)
            
            # Check if the user is verified
            if not user.is_verified:
                return ResponseHandler.failure(
                    message=EMAIL_NOT_VERIFIED,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Generate OTP and save to user profile
            user.otp = random.randint(100000, 999999)
            user.save()

            # Prepare context for sending OTP email
            context = {
                "subject": "Forgot Password mail",
                "code": user.otp,
                "email": user.email,
                'protocol': 'http',
            }

            # Start email thread for sending OTP
            t = threading.Thread(target=send_forgot_password_mail, args=[email, context])
            t.setDaemon(True)
            t.start()

            # Return success response
            return ResponseHandler.success(
                message=MAIL_SENT_SUCCESS,
                status_code=status.HTTP_201_CREATED
            )

        except Exception as error:
            # Handle unexpected errors
            return ResponseHandler.failure(
                message=str(error),
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
class ConfirmPasswordViewSet(nBaseViewset):
    """Viewset to handle password change request after OTP validation."""
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Allows the user to change their password after OTP validation.",
        request_body=ChangePasswordSerializer,
        responses={
            status.HTTP_200_OK: PASSWORD_UPDATE_SUCCESS,
            status.HTTP_400_BAD_REQUEST:INVALID_OTP,
            status.HTTP_500_INTERNAL_SERVER_ERROR: HTTP_500_INTERNAL_SERVER_ERROR
        },
        tags=['User Authentication']

    )
    def create(self, request, *args, **kwargs):
        """Change the user's password after validating the OTP."""
        try:
            data = request.data
            email = data.get('email')
            otp = data.get('otp')
            new_password = data.get('new_password')

            # Fetch the user by email
            user = self.queryset.get(email=email)

            # Validate OTP
            if user.otp != otp:
                return ResponseHandler.failure(
                    message=INVALID_OTP,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            password_validation = password_check(data["new_password"])

            # Change the password and clear the OTP
            user.set_password(new_password)
            user.otp = None
            user.save()

            # Return success response
            return ResponseHandler.success(
                message=PASSWORD_UPDATE_SUCCESS,
                status_code=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            # Handle case where user is not found
            return ResponseHandler.failure(
                message=USER_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as error:
            # Catch any other unexpected errors
            return ResponseHandler.failure(
                message=str(error),
                status_code=status.HTTP_400_BAD_REQUEST
            )