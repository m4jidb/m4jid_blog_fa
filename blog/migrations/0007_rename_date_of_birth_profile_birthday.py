# Generated by Django 4.2.5 on 2023-10-02 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_profile_date_of_birth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='date_of_birth',
            new_name='birthday',
        ),
    ]
