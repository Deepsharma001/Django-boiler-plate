from rest_framework import serializers
from apps.users.models import User
from datetime import date

class UpdateUserSerializer(serializers.Serializer):
    """
    Serializer for updating user profiles.
    """
    GENDER_CHOICES = (
        ('M', 'M'),
        ('F', 'F'),
        ('O', 'O'),
        ('X', 'X'),
    )

    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)
    number = serializers.CharField(required=False, max_length=15)
    gender = serializers.ChoiceField(
        required=False, 
        choices=GENDER_CHOICES
    )
    profile_photo = serializers.ImageField(required=False)
    date_of_birth = serializers.DateField(required=False)

    def validate_number(self, value):
        """
        Validate that the phone number contains only digits and has a valid length.
        """
        if not value.isdigit():
            raise serializers.ValidationError("The phone number must contain only digits.")
        if len(value) < 7 or len(value) > 15:
            raise serializers.ValidationError("The phone number must be between 7 and 15 digits.")
        return value

    def validate_date_of_birth(self, value):
        """
        Validate that the date of birth is not in the future.
        """
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def update(self, instance, validated_data):
        """
        Update the user instance with the validated data.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'profile_photo' in validated_data:
            instance.profile_photo = validated_data['profile_photo']
        instance.phone_number = validated_data.get('number', instance.phone_number)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()
        return instance