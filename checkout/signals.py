from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderItems

@receiver(post_save, sender=OrderItems)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on order items update/create
    """
    instance.order.update_total()

@receiver(post_delete, sender=OrderItems)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on order items delete
    """
    instance.order.update_total()