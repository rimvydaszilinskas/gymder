# Generated by Django 2.2.7 on 2019-11-13 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_activity_is_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='activities.Activity'),
        ),
        migrations.AlterField(
            model_name='request',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
