# Generated by Django 3.0.7 on 2023-06-01 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20230601_1243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='userProfile',
        ),
    ]
