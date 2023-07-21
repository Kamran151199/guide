from rest_framework import permissions


class IsInCompany(permissions.BasePermission):
    """
    This is an object level permission class
    that checks if the user is in the company.
    This has to be used in conjunction with the
    Model level permission class.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.company == obj

    def has_permission(self, request, view):
        return request.user.is_authenticated
