from rest_framework import serializers
from apps.users.models import User


class SignupUserSerializers(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

class VerifyUserRequestSerializer(serializers.Serializer):
    """Serializer to validate the request body with uid and token."""
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)