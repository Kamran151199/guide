from django.apps import AppConfig


class MailerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "services.mailer"

    def ready(self):
        from services.mailer.signals import security  # noqa: 401
