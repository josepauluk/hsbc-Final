from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, AccessToken


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "first_name", "last_name",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        ("Information", {"fields": ("first_name", "last_name")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "first_name", "last_name",
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

# class AccessTokenAdmin(admin.ModelAdmin):
#     list_display = ( 'token', 'owner',
#         'is_active', 'shortcut_hash', 'created_on', 'expires_on')

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(AccessToken, AccessTokenAdmin)
