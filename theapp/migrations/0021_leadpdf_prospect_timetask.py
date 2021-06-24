# Generated by Django 3.2.4 on 2021-06-23 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theapp', '0020_alter_document_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('full_name', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('biz_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prospect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biz_name', models.CharField(max_length=100, null=True, unique=True)),
                ('phone', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('link', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_desc', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('completed', models.BooleanField(default=False)),
                ('total_time', models.IntegerField(null=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
