# Generated by Django 5.1.1 on 2024-10-22 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qyfy', '0004_alter_delivery_person_receiving'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='invoice_file',
            field=models.FileField(blank=True, null=True, upload_to='invoices/'),
        ),
    ]