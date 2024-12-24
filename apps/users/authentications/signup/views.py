from base64 import urlsafe_b64encode
import threading
from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import status
from django.db import transaction
from django.contrib.auth.models import Group
from apps.users.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.crypto import get_random_string
from core.baseviewset.viewset import nBaseViewset
from core.validators.email_password_validator import password_check, validate_email
from utils.send_email import send_welcome_mail
from apps.users.authentications.signup.serializers import SignupUserSerializers,VerifyUserRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from core.response_handler.handler import ResponseHandler
from utils.messages import *

class AuthSignupViewSet(nBaseViewset):
    """
    API ViewSet for user signup functionality. It handles the creation of a new user,
    validates the user input, and sends a verification email to the user asynchronously.
    """
    queryset = User.objects
    serializer_class = SignupUserSerializers
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Create a new user and send a verification email.",
        request_body=SignupUserSerializers,
        responses={
            status.HTTP_200_OK: NEW_USER_CREATED,
            status.HTTP_400_BAD_REQUEST: HTTP_400_BAD_REQUEST
        },
        tags=['User Authentication']

    )
    def create(self, request, *args, **kwargs):
        """
        Handle user registration. Validates email and password, creates a user, 
        sends a verification email, and adds the user to a group.
        """
        data = request.data

        try:
            with transaction.atomic():
                # Check if the email already exists
                if User.objects.filter(email=data["email"]).exists():
                    return ResponseHandler.failure(
                        message=USER_ALREADY_EXISTS,
                        status_code=status.HTTP_400_BAD_REQUEST
                    )

                # Validate email format
                email_validation_response = validate_email(data["email"])

                # Validate password
                password_validation = password_check(data["password"])

                # Create user
                user_data = self.create_user(data)

                # Send verification email asynchronously
                self.send_verification_email(request, user_data)

                # Add user to 'user' group
                self.add_user_to_group(user_data)

                return ResponseHandler.success(
                    data={"email": data["email"]},
                    message=NEW_USER_CREATED,
                    status_code=status.HTTP_200_OK
                )

        except Exception as error:
            return ResponseHandler.failure(
                message=str(error),
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    def create_user(self, data):
        """
        Creates a new user based on the provided data and returns the user object.
        """
        user = self.queryset.create(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data.get("last_name", ""),
            is_active=False,
            is_staff=False,
            is_superuser=False,
        )
        user.set_password(data["password"])
        user.save()
        return user

    def send_verification_email(self, request, user):
        """
        Sends an email with a verification link to the user asynchronously.
        This is done in a separate thread to avoid blocking the main request.
        """
        context = {
            "subject": "Welcome Email",
            "email": user.email,
            "uid": urlsafe_b64encode(force_bytes(user.pk)),
            "user": user,
            "token": default_token_generator.make_token(user),
            "protocol": 'http',
            "url": f"{request._current_scheme_host}/api/app/auth/verifyuser/{urlsafe_b64encode(force_bytes(user.pk)).decode('utf-8')}/{default_token_generator.make_token(user)}/",
        }

        t = threading.Thread(target=send_welcome_mail, args=[user.email, context])
        t.setDaemon(True)
        t.start()      

    def add_user_to_group(self, user):
        """
        Adds the user to the 'user' group. If the group doesn't exist, it will be created.
        """
        group, created = Group.objects.get_or_create(name='user')
        group.user_set.add(user)

class UserVerification(nBaseViewset):
    """
    API ViewSet to handle user email verification using the token sent during registration.
    It verifies the token and updates the user's verified status accordingly.
    """
    queryset = User.objects
    serializer_class = VerifyUserRequestSerializer
    http_method_names = ['post']
    
    
    def get_user(self, uidb64):
        """
        Decodes the base64-encoded user ID and retrieves the corresponding user object.
        """
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user
    
    @swagger_auto_schema(
        operation_description="Verify the user's email using the token sent during registration.",
        request_body=VerifyUserRequestSerializer,
        responses={
            status.HTTP_200_OK: ACCOUNT_VERIFIED_SUCCESSFULLY,
            status.HTTP_400_BAD_REQUEST: HTTP_400_BAD_REQUEST,
            status.HTTP_500_INTERNAL_SERVER_ERROR: HTTP_500_INTERNAL_SERVER_ERROR
        },
        tags=['User Authentication']

    )
    def create(self, request, *args, **kwargs):
        """
        Verifies the user's email using the provided token. If the token is valid, 
        the user's verified status is updated.
        """
        try:
            data = request.data
            uid = data['uid']
            token = data['token']
            user = self.get_user(uid)
            if not user:
                return ResponseHandler.failure(
                    message=EXPIRED_TOKEN,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if user.is_verified:
                return ResponseHandler.success(
                    message=ALREADY_ACCOUNT_VERIFIED
                )

            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                return ResponseHandler.success(
                    message=ACCOUNT_VERIFIED_SUCCESSFULLY
                )
            else:
                return ResponseHandler.failure(
                    message=EXPIRED_TOKEN,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        except Exception as error:
            return ResponseHandler.failure(
                message=str(error),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
