# Generated by Django 3.2.4 on 2021-06-23 20:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('theapp', '0024_timetask_agent'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TimeTask',
            new_name='TimeRecord',
        ),
    ]
