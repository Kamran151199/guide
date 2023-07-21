from django.contrib import admin
from services.user.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "is_staff",
        "is_active",
        "is_verified",
        "is_superuser",
        "date_joined",
        "last_login",
    )
    list_display_links = ("id", "username")
    list_filter = ("is_staff", "is_active", "is_superuser", "date_joined", "last_login")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)
    readonly_fields = ("id", "date_joined", "last_login")
    fields = (
        "id",
        "username",
        "email",
        "is_staff",
        "is_active",
        "is_verified",
        "is_superuser",
        "date_joined",
        "last_login",
    )
    list_per_page = 10
    list_max_show_all = 10
    list_editable = ("is_staff", "is_active", "is_verified", "is_superuser")
    list_select_related = True


admin.site.register(User, UserAdmin)
