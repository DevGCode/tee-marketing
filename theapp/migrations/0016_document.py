# Generated by Django 3.2.4 on 2021-06-16 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theapp', '0015_auto_20210616_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('upload', models.FileField(upload_to='team-documents/')),
            ],
        ),
    ]
