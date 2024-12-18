# Generated by Django 5.1.1 on 2024-12-05 07:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KENETAssets', '0014_assets_asset_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assets',
            options={'ordering': ['-id'], 'verbose_name': 'Asset', 'verbose_name_plural': 'Assets'},
        ),
        migrations.AlterModelOptions(
            name='checkout',
            options={'ordering': ['-checkout_date'], 'verbose_name': 'Dispatch List', 'verbose_name_plural': 'Dispatch Lists'},
        ),
        migrations.AlterField(
            model_name='assets',
            name='status',
            field=models.CharField(blank=True, choices=[('instore', 'In Store'), ('faulty', 'Faulty'), ('onsite', 'On Site'), ('decommissioned', 'Decommissioned'), ('pending_release', 'Pending Release'), ('pending_approval', 'Pending Approval '), ('approved', 'Approved by Admin '), ('rejected', 'Denied by Admin ')], default='instore', max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='SavedPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(upload_to='pdfs/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
