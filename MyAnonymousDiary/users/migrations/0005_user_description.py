# Generated by Django 2.1.1 on 2018-10-21 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20181021_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, max_length=800, null=True),
        ),
    ]
