# Generated by Django 5.1.5 on 2025-06-27 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_member_course_alter_stand_stand_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_image',
            field=models.ImageField(upload_to='midea/member_profiles/'),
        ),
        migrations.AlterField(
            model_name='stand',
            name='stand_cover',
            field=models.ImageField(upload_to='midea/stand_cover/'),
        ),
    ]
