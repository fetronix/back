# Generated by Django 5.1.1 on 2024-11-19 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KENETAssets', '0004_remove_assets_new_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='authorizing_name',
        ),
        migrations.RemoveField(
            model_name='checkout',
            name='verifier_user_approve',
        ),
    ]