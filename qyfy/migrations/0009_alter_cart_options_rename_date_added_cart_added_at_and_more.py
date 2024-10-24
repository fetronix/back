# Generated by Django 5.1.1 on 2024-10-23 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qyfy', '0008_alter_assets_new_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={},
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='date_added',
            new_name='added_at',
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('user', 'asset')},
        ),
    ]