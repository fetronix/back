# Generated by Django 5.1.1 on 2024-11-06 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KENETAssets', '0007_alter_cart_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReleaseAdminFormData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_name', models.CharField(max_length=255)),
                ('serial_number', models.CharField(max_length=100)),
                ('kenet_tag', models.CharField(max_length=100)),
                ('current_location', models.CharField(max_length=255)),
                ('new_location', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now=True)),
                ('quantity_required', models.PositiveIntegerField(default=1)),
                ('quantity_issued', models.PositiveIntegerField(default=1)),
                ('authorizing_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('signature_image', models.ImageField(blank=True, null=True, upload_to='signatures/')),
                ('authorization_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
