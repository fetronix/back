# Generated by Django 5.1.1 on 2024-12-05 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KENETAssets', '0016_remove_savedpdf_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='release_forms/'),
        ),
    ]