from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django_resized import ResizedImageField
from django.utils import timezone
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_user')
    phone = models.CharField(max_length=20, verbose_name='شماره تلفن')
    birthday = jmodels.jDateTimeField(null=True, blank=True, verbose_name='تاریخ تولد')
    address = models.CharField(max_length=250, verbose_name='آدرس')
    city = models.CharField(max_length=200, verbose_name='شهر')
    state = models.CharField(max_length=200, verbose_name='استان')
    country = models.CharField(max_length=200, verbose_name='کشور')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    is_verified = models.BooleanField(default=False, verbose_name='وضعیت تایید')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده')
    deleted_at = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ حذف')
    deleted_by = models.CharField(max_length=200, blank=True, verbose_name='حذف توسطِ')
    deleted_reason = models.CharField(max_length=200, blank=True, verbose_name='دلیل حذف')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'

    def __str__(self):
        return self.user.username


class ProfileImage(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile_images", verbose_name="پروفایل"
    )
    image_file = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        quality=75,
        upload_to='profile_img/',
        blank=True,
        verbose_name='تصویر پروفایل'
    )
    alt = models.CharField(max_length=250, blank=True, verbose_name='متن جایگزین')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    deleted_at = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ حذف')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        verbose_name = "تصویر پروفایل"
        verbose_name_plural = "تصاویر پروفایل"

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.alt if self.alt else "None"


class CustomTag(TagBase):
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"


class CustomCategory(TagBase):
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class TaggedPost(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CustomTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class CategorizedPost(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CustomCategory,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='منتشر شده')


class Post(models.Model):
    STATUS_CHOICES = [
        ('پیش نویس', 'پیش نویس'),
        ('منتشر شده', 'منتشر شده'),
        ('رد شده', 'رد شده'),
    ]

    title = models.CharField(max_length=200, verbose_name='عنوان')
    content = models.TextField(verbose_name='محتوا')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='نویسنده')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    published_at = jmodels.jDateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده')
    deleted_at = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ حذف')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='پیش نویس',
        verbose_name='وضعیت'
    )
    tags = TaggableManager(through=TaggedPost)
    categories = TaggableManager(through=CategorizedPost)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.is_deleted:
            self.deleted_at = timezone.now()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.post_images.all():
            if img.image_file:
                storage, path = img.image_file.storage, img.image_file.path
                storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_images", verbose_name="پروفایل")
    image_file = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        quality=75,
        upload_to='blog_post_img/',
        blank=True,
        verbose_name='تصویر پست'
    )
    alt = models.CharField(max_length=250, blank=True, verbose_name='متن جایگزین')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    deleted_at = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ حذف')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        verbose_name = "تصویر پست ها"
        verbose_name_plural = "تصاویر پست ها"

    def delete(self, *args, **kwargs):
        if self.image_file:
            storage = self.image_file.storage
            name = self.image_file.name
            storage.delete(name)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.alt if self.alt else "None"


class Comment(models.Model):
    STATUS_CHOICES = [
        ('یش نویس', 'پیش نویس'),
        ('منتشر شده', 'منتشر شده'),
        ('رد شده', 'رد شده'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='نویسنده')
    content = models.TextField(verbose_name='محتوا')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='یش نویس',
        verbose_name='وضعیت'
    )
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده')
    deleted_at = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ حذف')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'کامنت پست ها'
        verbose_name_plural = 'کامنت های پست ها'

    def __str__(self):
        return self.post.title


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('باز', 'باز'),
        ('بسته', 'بسته'),
        ('درحال بررسی', 'درحال بررسی'),
    ]

    PRIORITY_CHOICES = [
        ('کم', 'کم'),
        ('متوسط', 'متوسط'),
        ('بالا', 'بالا'),
    ]

    title = models.CharField(max_length=200, verbose_name='عنوان')
    content = models.TextField(verbose_name='محتوا')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tickets_created', verbose_name='نویسنده'
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tickets_assigned', null=True, blank=True,
        verbose_name='مسعول پاسخ'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='باز', verbose_name='وضعیت')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='متوسط', verbose_name='اولویت')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def delete(self, *args, **kwargs):
        for f in self.ticket_attachments.all():
            storage, path = f.file.storage, f.file.path
            storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


class TicketAttachment(models.Model):
    file = models.FileField(upload_to='ticket_attachments/', verbose_name='پیوست', null=True, blank=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_attachments')
    alt = models.CharField(max_length=250, blank=True, verbose_name='متن جایگزین برای پیوست')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    deleted_at = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ حذف')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        verbose_name = "پیوست تیکت ها"
        verbose_name_plural = "پیوست های تیکت ها"

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.alt if self.alt else "None"
