from rest_framework import serializers

from apps.users.models import UserSocialProfile


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)