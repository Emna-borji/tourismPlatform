# users/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Custom permission to allow only admin users to perform certain actions.
    Admins can create, update, and delete hotels, but they can't delete their own profile.
    """

    def has_permission(self, request, view):
        # Allow access only if the user is authenticated and is an admin
        return request.user and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        # Allow access for admins on any object
        if view.action in ['create', 'update', 'destroy']:  # Admin can perform these actions
            return request.user and request.user.role == 'admin'

        # Admin cannot delete their own profile
        if view.action == 'destroy':
            return obj != request.user
        
        return False
    

class IsReviewOwnerOrAdmin(BasePermission):
    """
    - Users and admins can create, update, and delete their own reviews.
    - Admins can delete other users' reviews, but not another admin's reviews.
    - Everyone can view reviews.
    """

    def has_permission(self, request, view):
        # Allow everyone to view reviews (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        # Only authenticated users can create, update, or delete reviews
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Everyone can view reviews
        if request.method in SAFE_METHODS:
            return True

        # Users and admins can update or delete their own reviews
        if obj.user == request.user:
            return True

        # Admins can delete another user's review, but not another admin's review
        if request.method == 'DELETE' and request.user.role == 'admin' and obj.user.role != 'admin':
            return True

        return False