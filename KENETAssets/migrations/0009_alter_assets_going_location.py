# Generated by Django 5.1.1 on 2024-11-29 06:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KENETAssets', '0008_assetsmovement_sent_to_erp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='going_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='going_location', to='KENETAssets.location'),
        ),
    ]
