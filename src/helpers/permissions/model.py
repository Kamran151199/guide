from rest_framework import permissions


class ModelPermissions(permissions.DjangoModelPermissions):
    """
    This class is used to override the default DjangoModelPermissions class
    to restrict the permissions of GET, OPTIONS and HEAD requests,
    which are not protected by default.
    """

    def __init__(self):
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]
        self.perms_map["OPTIONS"] = ["%(app_label)s.view_%(model_name)s"]
        self.perms_map["HEAD"] = ["%(app_label)s.view_%(model_name)s"]
        super().__init__()
