# Generated by Django 5.1.5 on 2025-04-24 19:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_id', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('project_description', models.TextField()),
                ('project_cover', models.ImageField(blank=True, null=True, upload_to='competitors/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competitors', to='api.category')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
                ('competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.competitor')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.voter')),
            ],
            options={
                'unique_together': {('voter', 'category')},
            },
        ),
    ]
