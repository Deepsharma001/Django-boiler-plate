from rest_framework import routers
from django.urls import path
from apps.users.authentications.forgotpassword.forgotpassword import  ForgotPasswordViewSet, ConfirmPasswordViewSet
from apps.users.authentications.login.views import AuthLoginViewSet, AuthLogoutViewSet
from apps.users.authentications.resetpassword.resetpassword import ResetPasswordViewSet
from apps.users.authentications.signup.views import AuthSignupViewSet, UserVerification
from apps.users.views import ManageProfile

router = routers.DefaultRouter()

router.register(r'auth/register', AuthSignupViewSet)
router.register(r'auth/login', AuthLoginViewSet)
router.register(r'auth/logout', AuthLogoutViewSet)
router.register(r'auth/forgot_password', ForgotPasswordViewSet)
router.register(r'auth/confirm_password', ConfirmPasswordViewSet)
router.register(r'auth/verify_user', UserVerification)
router.register(r'auth/reset_password', ResetPasswordViewSet)
router.register(r'auth/manage_profile', ManageProfile)
