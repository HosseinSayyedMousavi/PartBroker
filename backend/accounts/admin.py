from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils import timezone
# Register your models here.


class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for user management with add and change forms plus password
    """

    model = User
    list_display = ("phone_number","email", "is_superuser", "is_active")
    list_filter = ("email", "is_superuser", "is_active", )
    searching_fields = ("email",)
    ordering = ("email",)
    readonly_fields =("last_login","created_date","updated_date")
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("phone_number", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser"
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "important dates",
            {
                "fields": ("last_login","created_date","updated_date"),
            },
        ),
        (
            "other fields",
            {
                "fields": ("email","first_name","last_name"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )

admin.site.register(User,CustomUserAdmin)