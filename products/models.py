from django.db import models

# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Product(models.Model):
    categories = models.ManyToManyField('Category')
    product_id = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    bedframe_sizes = models.BooleanField(default=False, null=True, blank=True)
    dimensions_height = models.CharField(max_length=100, default='0')
    dimensions_width = models.CharField(max_length=100, default='0')
    dimensions_depth = models.CharField(max_length=100, default='0')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name