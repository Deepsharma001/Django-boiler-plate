from rest_framework import serializers

class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128,required=True)
    new_password = serializers.CharField(max_length=128,required=True)
    