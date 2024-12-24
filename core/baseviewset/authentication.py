from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed


class cTokenAuthentication(TokenAuthentication):
    """
    Custom token authentication class that uses the 'Bearer' keyword and checks token validity.
    
    This class overrides the `authenticate_credentials` method to:
    - Validate if the token exists.
    - Check if the user is active.
    - Handle token expiration and renewal.
    """
    keyword = 'Bearer'  # Specifies the authentication keyword used in the Authorization header.

    def authenticate_credentials(self, key):
        """
        Authenticate the given token key.

        Args:
            key (str): The token key provided by the client in the 'Authorization' header.

        Returns:
            tuple: A tuple containing the authenticated user and the token object.

        Raises:
            AuthenticationFailed: If the token is invalid, or the user is not active.
        """
        try:
            # Retrieve the token object using the provided key.
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            # If the token doesn't exist, raise an authentication error.
            raise AuthenticationFailed("Invalid Token")

        # Check if the user associated with the token is active.
        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")

        # Check if the token has expired and handle renewal if necessary.
        is_expired, token = token_expire_handler(token)

        # Return the authenticated user and token.
        return token.user, token


def is_token_expired(token):
    """
    Check if the token is expired based on the user's last login time.
    
    Args:
        token (Token): The token object to check for expiration.

    Returns:
        bool: True if the token is expired, False otherwise.
    """
    # Retrieve the user's last login time.
    user_last_login = Token.objects.get(key=token).user.last_login
    if user_last_login:
        # Compare the last login time to the current time.
        today = timezone.now()
        # If the user hasn't logged in for 7 or more days, consider the token expired.
        if (today - user_last_login).days >= 7:
            return True
        else:
            return False
    else:
        # If there's no last login time, consider the token expired.
        return False


def token_expire_handler(token):
    """
    Handle the expiration of the token, renewing it if necessary.

    Args:
        token (Token): The token object to check and potentially renew.

    Returns:
        tuple: A tuple with a boolean indicating expiration and the (possibly renewed) token.
    """
    # Check if the token has expired.
    is_expired = is_token_expired(token)
    if is_expired:
        # If expired, delete the old token and create a new one.
        token.delete()
        token = Token.objects.create(user=token.user)
    # Return the expiration status and the updated token.
    return is_expired, token
