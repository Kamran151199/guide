from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "services.user"

    def ready(self):
        import services.user.signals.user  # noqa: F401 pylint: disable=unused-import
