from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, UserAddress

# Register your models here.

"""
Admin configuration for managing User Profile model.
"""
admin.site.register(UserProfile)

# Define UserAddressInline to include UserAddress fields in the UserProfile admin
class UserAddressInline(admin.StackedInline):
    model = UserAddress
    extra = 1  # Number of empty address forms to display

# Define UserProfileInline to include UserProfile fields in the User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    inlines = [UserAddressInline]  

# # Unregister the default UserAdmin
admin.site.unregister(User)

# # Extend the UserAdmin class to include UserProfileInline
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# # Register the UserAdmin
admin.site.register(User, CustomUserAdmin)

# Register the UserAddress model in the admin site
admin.site.register(UserAddress)