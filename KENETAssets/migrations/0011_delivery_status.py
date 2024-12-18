# Generated by Django 5.1.1 on 2024-11-29 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KENETAssets', '0010_rename_going_location_assets_destination_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='status',
            field=models.CharField(blank=True, choices=[('instore', 'In Store'), ('faulty', 'Faulty'), ('onsite', 'On Site'), ('faulty', 'Faulty'), ('decommissioned', 'Decommissioned'), ('pending_release', 'Pending Release'), ('pending_approval', 'Pending Approval '), ('approved', 'Approved by Admin '), ('rejected', 'Denied by Admin ')], default='instore', max_length=20, null=True),
        ),
    ]
