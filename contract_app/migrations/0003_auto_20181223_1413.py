# Generated by Django 2.1.4 on 2018-12-23 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contract_app', '0002_auto_20181223_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='contract_app.Role'),
        ),
    ]