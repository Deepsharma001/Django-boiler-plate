from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        try:
            for group in Group.objects.all():
                self.ensure_group_permissions(group)

            response = self.get_response(request)
        except Exception as e:
            print(f"An error occurred while checking permissions: {e}")
            return self.get_response(request)  # Return response to the client as is

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def ensure_group_permissions(self, group):
        # Get all available permissions
        all_permissions = Permission.objects.all()

        # Get current permissions for the group
        current_permissions = group.permissions.all()

        # Find missing permissions
        missing_permissions = set(all_permissions) - set(current_permissions)

        # Add missing permissions to the group
        if missing_permissions:
            group.permissions.add(*missing_permissions)
            print(f"Added {len(missing_permissions)} permissions to group '{group.name}'")