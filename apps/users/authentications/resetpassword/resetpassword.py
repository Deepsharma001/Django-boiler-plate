
from rest_framework import status
from django.db import transaction
from apps.users.models import User
from core.baseviewset.viewset import aBaseViewset
from core.validators.email_password_validator import password_check
from apps.users.authentications.resetpassword.serializers import PasswordResetSerializer
from rest_framework.serializers import Serializer  
from drf_yasg.utils import swagger_auto_schema
from core.response_handler.handler import ResponseHandler
from utils.messages import *

class ResetPasswordViewSet(aBaseViewset):
    """Viewset to handle password reset after old password validation."""
    queryset = User.objects
    serializer_class = PasswordResetSerializer
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Allows the user to reset their password after validating the old password.",
        request_body=PasswordResetSerializer,
        responses={
            status.HTTP_201_CREATED: PASSWORD_UPDATE_SUCCESS,
            status.HTTP_400_BAD_REQUEST: HTTP_400_BAD_REQUEST,
            status.HTTP_500_INTERNAL_SERVER_ERROR: HTTP_500_INTERNAL_SERVER_ERROR
        },
        tags=['User Authentication']
    )
    def create(self, request, *args, **kwargs):
        """Reset the user's password after validating the old password."""
        try:
            old_password = request.data['old_password']
            new_password = request.data['new_password']
            if not request.user.check_password(old_password):
                # Old password does not match
                return ResponseHandler.failure(
                    message=OLD_PASSWORD_VALIDATION,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            if old_password == new_password:
                # New password cannot be the same as old password
                return ResponseHandler.failure(
                    message=NEW_PASSWORD_CANNOT_SAME_AS_OLD,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            # Validate new password
            password_validation = password_check(new_password)
            
            with transaction.atomic():
                user = User.objects.get(id=request.user.id)
                user.set_password(new_password)
                user.save()

            # Return success response
            return ResponseHandler.success(
                message=PASSWORD_UPDATE_SUCCESS,
                status_code=status.HTTP_201_CREATED
            )

        except Exception as error:
            # Handle unexpected errors
            return ResponseHandler.failure(
                message=str(error),
                status_code=status.HTTP_400_BAD_REQUEST
            )
