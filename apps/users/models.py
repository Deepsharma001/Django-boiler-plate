from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from utils.choices import SocialChoices

# Custom manager for the User model
class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model to handle user and superuser creation.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

# Custom User model that extends AbstractUser
class User(AbstractUser):
    """
    user model that replaces the default User model. 
    Supports email-based authentication and adds additional fields such as UUID, profile photo, and device type.
    """
    USER_TYPE_CHOICES = (
        (1, 'SuperAdmin'),
        (2, 'CompanyAdmin'),
        (3, 'User'),
    )
    DEVICE_TYPE_CHOICES = (
        (1, 'Android'),
        (2, 'iOS'),
        (3, 'Web'),
    )
    GENDER_CHOICES = (
        ('M', 'M'),
        ('F', 'F'),
        ('O', 'O'),
        ('X', 'X'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_photo = models.ImageField(
        upload_to='users/photos/', default="user.png", null=True, blank=True, verbose_name=_("Profile Photo")
    )
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    fcm_token = models.TextField(null=True, blank=True)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=3)
    device_type = models.IntegerField(choices=DEVICE_TYPE_CHOICES, default=3)
    otp = models.IntegerField(null=True, blank=True, default=None)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=1, null=True, blank=True, default=None)
    username = None  # Removes the username field from the parent class
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for updates
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Model to store social media information for the user
class UserSocialProfile(models.Model):
    """
    Represents a user's social media profile. 
    Stores information about the user's associated social platform and profile details.
    """
    user = models.OneToOneField(
        User, related_name="social_profile", on_delete=models.CASCADE
    )
    social_platform = models.CharField(
        max_length=30, choices=SocialChoices.choices()
    )
    social_type = models.CharField(
        max_length=30,
        choices=SocialChoices.choices()
    )
    social_id = models.CharField(max_length=255, null=True, blank=True)
    twitter_username = models.CharField(max_length=255, null=True, blank=True)
    instagram_username = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for updates

    class Meta:
        db_table = "user_social_profiles"

# Model to store information about password reset tokens
class ForgotPasswordToken(models.Model):
    """
    Represents a password reset token for a user. 
    Used to securely handle password recovery.
    """
    token = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forgot_password_tokens")
    expiry_time = models.DateTimeField()

    class Meta:
        db_table = "forgot_password_tokens"
