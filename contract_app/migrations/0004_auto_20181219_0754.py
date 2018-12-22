# Generated by Django 2.1.4 on 2018-12-19 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract_app', '0003_auto_20181217_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('can_read_contracts', models.BooleanField(default=False)),
                ('can_write_contracts', models.BooleanField(default=False)),
                ('can_countersign', models.BooleanField(default=False)),
                ('can_set_countersign', models.BooleanField(default=False)),
                ('can_review', models.BooleanField(default=False)),
                ('can_set_review', models.BooleanField(default=False)),
                ('can_sign', models.BooleanField(default=False)),
                ('can_set_sign', models.BooleanField(default=False)),
                ('can_read_users', models.BooleanField(default=False)),
                ('can_write_users', models.BooleanField(default=False)),
                ('can_read_roles', models.BooleanField(default=False)),
                ('can_write_roles', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='roles',
            field=models.ManyToManyField(related_name='users', to='contract_app.Role'),
        ),
    ]