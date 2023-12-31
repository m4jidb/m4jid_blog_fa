# Generated by Django 4.2.5 on 2023-09-28 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('content', models.TextField(verbose_name='محتوا')),
                ('post_image', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, quality=75, scale=None, size=[500, 500], upload_to='media/post_images', verbose_name='تصویر پست')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='حذف شده')),
                ('deleted_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ حذف')),
                ('status', models.CharField(choices=[('یش نویس', 'پیش نویس'), ('منتشر شده', 'منتشر شده'), ('رد شده', 'رد شده')], default='draft', max_length=10, verbose_name='وضعیت')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
            ],
            options={
                'verbose_name': 'پست',
                'verbose_name_plural': 'پست ها',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='محتوا')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('rejected', 'Rejected')], default='draft', max_length=10, verbose_name='وضعیت')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='ثأطح انجام')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='حذف شده')),
                ('deleted_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ حذف')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='پست')),
            ],
            options={
                'verbose_name': 'کامنت',
                'verbose_name_plural': 'کامنت ها',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='محتوا')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('status', models.CharField(choices=[('باز', 'باز'), ('بسته', 'بسته'), ('درحال بررسی', 'درحال بررسی')], default='open', max_length=20, verbose_name='وضعیت')),
                ('priority', models.CharField(choices=[('کم', 'کم'), ('متوسط', 'متوسط'), ('بالا', 'بالا')], default='medium', max_length=20, verbose_name='اولویت')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets_assigned', to=settings.AUTH_USER_MODEL, verbose_name='مسعول پاسخ')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_created', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
            ],
            options={
                'verbose_name': 'تیکت',
                'verbose_name_plural': 'تیکت ها',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['-created_at'], name='blog_ticket_created_39af8a_idx')],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, verbose_name='شماره تلفن')),
                ('profile_image', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=75, scale=None, size=[500, 500], upload_to='media/profile_images', verbose_name='تصویر پروفایل')),
                ('address', models.CharField(max_length=100, verbose_name='آدرس')),
                ('city', models.CharField(max_length=100, verbose_name='شهر')),
                ('state', models.CharField(max_length=100, verbose_name='استان')),
                ('country', models.CharField(max_length=100, verbose_name='کشور')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('is_verified', models.BooleanField(default=False, verbose_name='وضعیت تایید')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='حذف شده')),
                ('deleted_at', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ حذف')),
                ('deleted_by', models.CharField(blank=True, max_length=100, verbose_name='حذف توسطِ')),
                ('deleted_reason', models.CharField(blank=True, max_length=100, verbose_name='دلیل حذف')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پروفایل',
                'verbose_name_plural': 'پروفایل ها',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['-created_at'], name='blog_profil_created_6bc67c_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-created_at'], name='blog_post_created_45f0c6_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['-created_at'], name='blog_commen_created_1f5393_idx'),
        ),
    ]
