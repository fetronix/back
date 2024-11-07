# Generated by Django 5.1.1 on 2024-11-07 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KENETAssets', '0010_delete_releaseadminformdata_delete_releaseformdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='status',
            field=models.CharField(blank=True, choices=[('instore', 'In Store'), ('faulty', 'Faulty'), ('onsite', 'On Site'), ('pending_release', 'Pending Release'), ('pending_approval', 'Pending Approval '), ('approved', 'Approved by Admin '), ('rejected', 'Denied by Admin ')], default='instore', max_length=20, null=True),
        ),
    ]