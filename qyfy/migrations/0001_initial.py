# Generated by Django 5.1.1 on 2024-09-25 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received', models.DateField(auto_now_add=True)),
                ('person_receiving', models.CharField(max_length=100)),
                ('asset_description', models.TextField()),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('kenet_tag', models.CharField(max_length=100, unique=True)),
                ('location', models.CharField(max_length=200)),
            ],
        ),
    ]
