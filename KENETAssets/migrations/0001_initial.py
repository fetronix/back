# Generated by Django 5.1.1 on 2024-10-31 09:58

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received', models.DateField(auto_now_add=True)),
                ('asset_description', models.TextField()),
                ('asset_description_model', models.CharField(blank=True, max_length=100, null=True)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('kenet_tag', models.CharField(max_length=100, unique=True)),
                ('new_location', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[('instore', 'In Store'), ('faulty', 'Faulty'), ('onsite', 'On Site'), ('pending_release', 'Pending Release')], default='instore', max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Assets',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('date_delivered', models.DateField(auto_now_add=True)),
                ('invoice_file', models.FileField(blank=True, null=True, upload_to='invoices/')),
                ('invoice_number', models.CharField(max_length=100)),
                ('project', models.CharField(max_length=255)),
                ('comments', models.TextField(blank=True)),
                ('delivery_id', models.CharField(blank=True, editable=False, max_length=10, unique=True)),
            ],
            options={
                'verbose_name': 'Delivery',
                'verbose_name_plural': 'Deliveries',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='ReleaseFormData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('current_location', models.CharField(max_length=255)),
                ('new_location', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('quantity_required', models.PositiveIntegerField()),
                ('quantity_issued', models.PositiveIntegerField()),
                ('serial_number', models.CharField(max_length=100)),
                ('kenet_tag', models.CharField(max_length=100)),
                ('authorizing_name', models.CharField(max_length=255)),
                ('authorization_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KENETAssets.assets')),
            ],
        ),
        migrations.AddField(
            model_name='assets',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='KENETAssets.category'),
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout_date', models.DateTimeField(auto_now_add=True)),
                ('expected_return_date', models.DateTimeField(blank=True, null=True)),
                ('actual_return_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('checked_out', 'Checked Out'), ('returned', 'Returned')], default='pending', max_length=20)),
                ('comments', models.TextField(blank=True, null=True)),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkout', to='KENETAssets.cart')),
            ],
        ),
        migrations.AddField(
            model_name='assets',
            name='delivery',
            field=models.ForeignKey(blank=True, help_text='Associated delivery for this asset', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assets', to='KENETAssets.delivery'),
        ),
        migrations.AddField(
            model_name='assets',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primary_location', to='KENETAssets.location'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='supplier_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primary_suppliers', to='KENETAssets.suppliers'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('network_admin', 'Network Admin'), ('noc_user', 'NOC User'), ('system_admin', 'System Admin'), ('network_engineer', 'Network Engineer')], default='noc_user', max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='delivery',
            name='person_receiving',
            field=models.ForeignKey(blank=True, help_text='User who received the asset', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assets',
            name='person_receiving',
            field=models.ForeignKey(blank=True, help_text='User who received the asset', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='AssetMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time of the movement')),
                ('comments', models.TextField(blank=True, help_text='Additional details about the movement', null=True)),
                ('assets', models.ManyToManyField(help_text='Assets being moved', related_name='movements', to='KENETAssets.assets')),
                ('destination_location', models.ForeignKey(blank=True, help_text='Location to where the asset is being moved', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movement_destination', to='KENETAssets.location')),
                ('source_location', models.ForeignKey(blank=True, help_text='Location from where the asset is being moved', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movement_source', to='KENETAssets.location')),
                ('person_moving', models.ForeignKey(blank=True, help_text='Person responsible for moving the asset', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Asset Movement',
                'verbose_name_plural': 'Asset Movements',
                'ordering': ['-movement_date'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('user', 'asset')},
        ),
    ]
