# Generated by Django 3.2.3 on 2021-05-18 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0002_rename_user_login_userlogin_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlogin',
            name='access_level',
        ),
    ]
