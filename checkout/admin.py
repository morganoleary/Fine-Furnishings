from django.contrib import admin
from .models import Order, OrderItems

# Register your models here.
class OrderItemsAdminInline(admin.TabularInline):
    model = OrderItems
    readonly_fields = ('order_items_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemsAdminInline,)

    readonly_fields = ('order_number', 'order_date',
                       'delivery_charge', 'product_total',
                       'order_total', 'user_profile',)
    
    fields = ('order_number', 'user_profile',
              'address', 'order_date',
              'delivery_charge', 'product_total',
              'order_total',)
    
    list_display = ('order_number', 'user_profile',
                    'order_date', 'delivery_charge',
                    'product_total', 'order_total',)
    
    ordering = ('-order_date',)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems)