# Generated by Django 5.1.1 on 2024-11-18 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KENETAssets', '0003_checkout_verifier_user_approve'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assets',
            name='new_location',
        ),
        migrations.AlterField(
            model_name='assets',
            name='going_location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]