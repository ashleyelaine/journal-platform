# Generated by Django 2.1.1 on 2018-10-21 20:00

import MyAnonymousDiary.users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.FileField(blank=True, null=True, upload_to=MyAnonymousDiary.users.models.user_directory_path),
        ),
    ]
