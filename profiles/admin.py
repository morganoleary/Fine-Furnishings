from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

# Register your models here.

"""
Admin configuration for managing User Profile model.
"""
admin.site.register(UserProfile)

# Define UserProfileInline to include UserProfile fields in the User admin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

# # Unregister the default UserAdmin


admin.site.unregister(User)

# # Extend the UserAdmin class to include UserProfileInline


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# # Register UserAdmin


admin.site.register(User, CustomUserAdmin)