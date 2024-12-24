from rest_framework import serializers

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

        
class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.IntegerField(required=True)
    new_password = serializers.CharField(max_length=15, required=True)
