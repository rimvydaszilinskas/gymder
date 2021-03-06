# Generated by Django 2.2.7 on 2019-11-06 20:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utils', '0002_address_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('duration', models.IntegerField(default=60, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(600)])),
                ('public', models.BooleanField(default=True)),
                ('needs_approval', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupActivity',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activities.Activity')),
                ('max_attendees', models.IntegerField(default=60, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(500)])),
                ('price', models.DecimalField(decimal_places=4, max_digits=12)),
                ('currency', models.CharField(choices=[('dkk', 'Danish Krona'), ('sek', 'Swedish Krona'), ('nok', 'Norwegian Krona'), ('eur', 'Euros'), ('gbp', 'Pounds'), ('usd', 'US Dollars'), ('cad', 'Canadian Dollars')], default='dkk', max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=('activities.activity',),
        ),
        migrations.CreateModel(
            name='IndividualActivity',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activities.Activity')),
            ],
            options={
                'abstract': False,
            },
            bases=('activities.activity',),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('denied', 'Denied')], default='pending', max_length=12)),
                ('message', models.TextField(blank=True, null=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.Activity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to='activities.ActivityType'),
        ),
        migrations.AddField(
            model_name='activity',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.Group'),
        ),
        migrations.AddField(
            model_name='activity',
            name='tags',
            field=models.ManyToManyField(related_name='activities', to='utils.Tag'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL),
        ),
    ]
