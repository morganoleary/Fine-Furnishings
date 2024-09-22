import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from profiles.models import UserProfile, UserAddress
from products.models import Product

# Create your models here.
class Order(models.Model):
    """
    A model representing a user's order
    """
    order_number = models.CharField(max_length=50, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL, related_name='orders')
    address = models.ForeignKey(UserAddress, on_delete=models.PROTECT)
    product_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=30)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.EmailField(blank=True, null=True)
    user_phone = models.CharField(max_length=50, blank=True, null=True)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    class Meta:
        unique_together = ('user_profile', 'order_number')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()
    
    def update_order_total(self):
        """
        Update the order total each time a line item is added,
        including the delivery fee.
        """
        self.product_total = self.order_items.aggregate(Sum('order_items_total'))['order_items_total__sum'] or 0
        self.delivery_charge = settings.STANDARD_DELIVERY_FEE

        self.order_total = self.product_total + self.delivery_charge
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Order Number: {self.order_number}"


class OrderItems(models.Model):
    """
    A model representing each item within an order
    """
    order = models.ForeignKey(Order, null=False, blank=False, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.PROTECT)
    bedframe_size = models.CharField(max_length=10, null=True, blank=True) # 3', 4', 4'6", 5', 6'
    quantity = models.IntegerField(null=False, blank=False, default=0)
    order_items_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    class Meta:
        unique_together = ('order', 'product')

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order items total
        and update the order total.
        """
        self.order_items_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Product ID: {self.product.product_id} on Order {self.order.order_number}"
