# Generated by Django 2.2.7 on 2019-12-16 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_auto_20191111_2107'),
        ('users', '0002_apitoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='followers', to='utils.Tag'),
        ),
    ]
