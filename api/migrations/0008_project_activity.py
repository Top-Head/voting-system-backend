# Generated by Django 5.1.5 on 2025-05-02 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_activity_remove_category_finished_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='api.activity'),
        ),
    ]
