# Generated by Django 3.2.4 on 2021-06-16 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theapp', '0019_alter_document_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='upload',
            field=models.FileField(upload_to='team-documents/'),
        ),
    ]
