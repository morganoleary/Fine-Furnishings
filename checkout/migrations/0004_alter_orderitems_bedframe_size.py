# Generated by Django 3.2.9 on 2024-08-05 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20240729_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='bedframe_size',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]