# Generated by Django 5.1.1 on 2024-11-05 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KENETAssets', '0003_remove_checkout_cart_items_checkout_cart_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='status',
            field=models.CharField(blank=True, choices=[('instore', 'In Store'), ('faulty', 'Faulty'), ('onsite', 'On Site'), ('pending_release', 'Pending Release'), ('pending_release_cart', 'Pending Release Cart')], default='instore', max_length=20, null=True),
        ),
    ]
