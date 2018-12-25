# Generated by Django 2.1.4 on 2018-12-24 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract_app', '0005_auto_20181224_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='can_read_roles',
        ),
        migrations.RemoveField(
            model_name='role',
            name='can_read_users',
        ),
        migrations.RemoveField(
            model_name='role',
            name='can_write_roles',
        ),
        migrations.RemoveField(
            model_name='role',
            name='can_write_users',
        ),
        migrations.AddField(
            model_name='role',
            name='can_manage_roles',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='can_manage_users',
            field=models.BooleanField(default=False),
        ),
    ]