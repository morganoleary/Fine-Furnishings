# Generated by Django 3.2.9 on 2024-09-22 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_image'),
        ('profiles', '0005_auto_20240731_2220'),
        ('checkout', '0005_auto_20240806_2124'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='order',
            unique_together={('user_profile', 'order_number')},
        ),
        migrations.AlterUniqueTogether(
            name='orderitems',
            unique_together={('order', 'product')},
        ),
    ]