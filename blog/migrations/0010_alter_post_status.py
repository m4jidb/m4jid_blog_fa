# Generated by Django 4.2.5 on 2023-10-08 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_post_published_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('پیش نویس', 'پیش نویس'), ('منتشر شده', 'منتشر شده'), ('رد شده', 'رد شده')], default='پیش نویس', max_length=10, verbose_name='وضعیت'),
        ),
    ]
