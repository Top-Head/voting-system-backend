# Generated by Django 5.1.5 on 2025-04-27 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_voter_groups_voter_is_active_voter_is_staff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voter',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='password',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='user_permissions',
        ),
    ]
