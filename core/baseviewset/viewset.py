from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from core.baseviewset.authentication import cTokenAuthentication
from core.baseviewset import rData

class AuthPerm(DjangoModelPermissions):
    """
    Custom permission class inheriting DjangoModelPermissions.
    
    Maps HTTP methods to the corresponding Django model permission codes.
    Can be customized to include additional permissions such as 'view' or 
    completely override permission mappings as needed.
    """
    # Mapping of HTTP methods to permission codes.
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],  # Maps GET requests to 'view' permissions.
        'OPTIONS': [],  # No permissions required for OPTIONS.
        'HEAD': [],  # No permissions required for HEAD.
        'POST': ['%(app_label)s.add_%(model_name)s'],  # Maps POST requests to 'add' permissions.
        'PUT': ['%(app_label)s.change_%(model_name)s'],  # Maps PUT requests to 'change' permissions.
        'PATCH': ['%(app_label)s.change_%(model_name)s'],  # Maps PATCH requests to 'change' permissions.
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],  # Maps DELETE requests to 'delete' permissions.
    }

class aBaseViewset(viewsets.ModelViewSet):
    """
    Custom base viewset that enforces token authentication and permissions.
    
    Overrides key methods (list, retrieve, create, update, destroy) to:
    - Assign the request object to the shared `rData.request`.
    - Preserve the base behavior of the parent class's methods.
    """
    # Use custom token-based authentication.
    authentication_classes = [cTokenAuthentication]
    # Apply custom permission class for authorization.
    permission_classes = [AuthPerm]

    def list(self, request, *args, **kwargs):
        """
        Handles GET requests to list objects.
        """
        rData.request = request  # Store the request object in a shared variable.
        return super().list(request, *args, **kwargs)  # Call the parent method.

    def retrieve(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve a single object.
        """
        rData.request = request
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new object.
        """
        rData.request = request
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Handles PUT or PATCH requests to update an existing object.
        """
        rData.request = request
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Handles DELETE requests to remove an object.
        """
        rData.request = request
        return super().destroy(request, *args, **kwargs)

class nBaseViewset(viewsets.ModelViewSet):
    """
    Simplified base viewset that overrides create, update, and destroy methods.
    
    These methods assign the request object to `rData.request` for potential
    shared use before calling the parent class's methods.
    """

    def create(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new object.
        """
        rData.request = request
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Handles PUT or PATCH requests to update an existing object.
        """
        rData.request = request
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Handles DELETE requests to remove an object.
        """
        rData.request = request
        return super().destroy(request, *args, **kwargs)
