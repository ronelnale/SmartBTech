# Generated by Django 5.1.1 on 2024-09-05 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartbtech', '0002_users_groups_users_is_active_users_is_staff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='users',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='users',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='users',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='users',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='users',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=50),
        ),
    ]
