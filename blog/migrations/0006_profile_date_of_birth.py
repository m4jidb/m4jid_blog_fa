# Generated by Django 4.2.5 on 2023-09-30 11:02

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_profile_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='تاریخ تولد'),
        ),
    ]
