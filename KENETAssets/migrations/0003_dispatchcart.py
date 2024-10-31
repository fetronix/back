# Generated by Django 5.1.1 on 2024-10-31 12:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KENETAssets', '0002_order_orderitem_delete_checkout'),
    ]

    operations = [
        migrations.CreateModel(
            name='DispatchCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_name', models.CharField(max_length=255)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('tag_number', models.CharField(max_length=100, unique=True)),
                ('location', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('dispatched', 'Dispatched')], default='pending', max_length=20)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dispatch_carts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dispatch Cart Item',
                'verbose_name_plural': 'Dispatch Cart Items',
                'unique_together': {('user', 'serial_number')},
            },
        ),
    ]
