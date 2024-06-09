from django.contrib import admin
from .models import ContactRequest

# Register your models here.

"""
Admin configuration for managing Contact Request model.
"""
admin.site.register(ContactRequest)