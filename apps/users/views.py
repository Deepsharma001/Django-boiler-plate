from core.baseviewset.viewset import aBaseViewset
from apps.users.models import User
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.users.serializers import UpdateUserSerializer
from core.response_handler.handler import ResponseHandler
from utils.messages import *

class ManageProfile(aBaseViewset):
    """
    Viewset for managing user profiles. Supports listing and updating profiles.
    """
    queryset = User.objects
    serializer_class = UpdateUserSerializer
    http_method_names = ['get','post']

    @swagger_auto_schema(
        operation_description="Retrieve the profile of the currently logged-in user.",
        request_body = None,
        responses={
            status.HTTP_200_OK: DETAILS_FETCH_SUCCESSFULLY,
            status.HTTP_400_BAD_REQUEST: HTTP_400_BAD_REQUEST
        },
        tags=['User Profile']
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve the profile of the currently logged-in user.
        """
        try:
            user = self.queryset.get(id=request.user.id)
            serialized_data = self.serializer_class(user).data
            return ResponseHandler.success(
                data=serialized_data,
                message=DETAILS_FETCH_SUCCESSFULLY,
                status_code=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return ResponseHandler.failure(
                message=USER_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as error:
            return ResponseHandler.failure(
                message=str(error),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Update the profile of the currently logged-in user.",
        request_body=UpdateUserSerializer,
        responses={
            status.HTTP_200_OK: DETAILS_UPDATED_SUCCESSFULLY,
            status.HTTP_400_BAD_REQUEST: HTTP_400_BAD_REQUEST,
            status.HTTP_500_INTERNAL_SERVER_ERROR: HTTP_500_INTERNAL_SERVER_ERROR
        },
        tags=['User Profile']
    )
    def create(self, request, *args, **kwargs):
        """
        Update the profile of the currently logged-in user.
        """
        try:
            # Pass the request data to the serializer
            user = self.queryset.get(id=request.user.id)
            serializer = self.serializer_class(user, data=request.data, partial=True)  # `partial=True` allows updates for some fields

            # Validate and save data
            if serializer.is_valid():
                serializer.save()
                return ResponseHandler.success(
                    data=serializer.data,
                    message="User updated successfully.",
                    status_code=status.HTTP_200_OK
                )
            else:
                return ResponseHandler.failure(
                    message=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        except User.DoesNotExist:
            return ResponseHandler.failure(
                message=USER_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as error:
            return ResponseHandler.failure(
                message=str(error),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )