# Generated by Django 3.2.9 on 2024-06-13 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20240603_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='bedframe_sizes',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]