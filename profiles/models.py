from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.


class UserProfile(models.Model):
    """
    Model representing a user of the site.
    """
    user_id = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=50)
    wishlist = models.ManyToManyField(Product, blank=True, related_name='wishlist_profiles')

    def __str__(self):
        return f"{self.user_id}"


class UserAddress(models.Model):
    """
    Model representing the authenticated user's address(es)
    """
    user_profile = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL, related_name='addresses')
    address_name = models.CharField(max_length=50)
    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255, blank=True, null=True)
    town_city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_name}: {self.street_address_1}, {self.town_city}, {self.country}"


class Wishlist(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_profile', 'product')

    def __str__(self):
        return f"{self.user_profile.user_id.username}'s wishlist item: {self.product.name}"