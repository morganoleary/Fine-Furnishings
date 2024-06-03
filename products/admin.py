from django.contrib import admin
from .models import Product, Category

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_id',
        'name',
        'price',
        'image',
    )

    ordering = ('product_id',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)