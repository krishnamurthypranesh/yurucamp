from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authn.models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = ((None, {"fields": ("username", "contact_email", "last_login_at")}),)
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email",)}),)

    list_display = ("username", "contact_email", "last_login_at")
    list_filter = ()
    search_fields = (
        "username",
        "contact_email",
    )
    ordering = ("id",)


admin.site.register(User, UserAdmin)

# Register your models here.
