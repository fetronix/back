# Generated by Django 5.1.1 on 2024-10-31 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qyfy', '0012_suppliers_assets_asset_description_model_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assets',
            name='new_location',
        ),
    ]
