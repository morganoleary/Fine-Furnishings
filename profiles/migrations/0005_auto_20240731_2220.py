# Generated by Django 3.2.9 on 2024-07-31 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_image'),
        ('profiles', '0004_alter_useraddress_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlist_profiles', to='products.Product'),
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlists', to='profiles.userprofile')),
            ],
            options={
                'unique_together': {('user_profile', 'product')},
            },
        ),
    ]
