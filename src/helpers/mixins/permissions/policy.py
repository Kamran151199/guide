
"""
This file is part of the Yoona.ai project.
It contains the mixins for the permission policies.
"""


class PermissionPolicyMixin:
    """
    PermissionPolicyMixin is a mixin that allows you to specify different
    permission classes for different methods on a view.
    Make sure that the view has a `permission_classes_by_action` attribute
    """

    # pylint: disable=unresolved-reference
    def check_permissions(self, request):
        try:
            # This line is heavily inspired from `APIView.dispatch`.
            # It returns the method associated with an endpoint.
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
            handler
            and self.permission_classes_by_action  # noqa: unresolved reference
            and self.permission_classes_by_action.get(
                handler.__name__
            )  # noqa: unresolved reference
        ):
            self.permission_classes = self.permission_classes_by_action.get(
                handler.__name__
            )  # noqa

        super().check_permissions(request)  # noqa: unresolved reference
