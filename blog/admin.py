from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, ProfileImage, Post, PostImage, Category, Tag, Comment, Ticket, TicketAttachment
from django_jalali.admin.filters import JDateFieldListFilter


class ProfileImageInline(admin.TabularInline):
    model = ProfileImage
    extra = 1


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = (
        'phone', 'address', 'city', 'state', 'country', 'is_verified', 'is_deleted', 'deleted_by', 'deleted_reason')


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class TagInline(admin.TabularInline):
    model = Tag
    extra = 1


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_verified', 'is_deleted')
    list_filter = ('is_verified', 'is_deleted', ('created_at', JDateFieldListFilter))
    search_fields = ('user__username', 'phone', 'address', 'city', 'state', 'country')
    ordering = ('-created_at',)
    fields = (
        'user', 'phone', 'address', 'city', 'state', 'country', 'is_verified', 'is_deleted', 'deleted_by',
        'deleted_reason')
    readonly_fields = ('created_at', 'updated_at', 'deleted_by', 'deleted_reason')
    date_hierarchy = 'created_at'
    inlines = [ProfileImageInline]


@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'alt', 'created_at', 'deleted_at')
    list_filter = ('created_at', 'deleted_at', ('profile__created_at', JDateFieldListFilter))
    search_fields = ('profile__user__username', 'alt')
    ordering = ('-created_at',)
    fields = ('profile', 'image_file', 'alt', 'created_at', 'deleted_at')
    readonly_fields = ('created_at', 'deleted_at')
    date_hierarchy = 'created_at'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'published_at', 'is_deleted')
    list_filter = ('status', 'is_deleted', ('created_at', JDateFieldListFilter), ('published_at', JDateFieldListFilter))
    search_fields = ('title', 'content', 'author__username', 'slug')
    ordering = ('-created_at',)
    fields = (
        'title', 'content', 'author', 'slug', 'created_at', 'published_at', 'updated_at', 'is_deleted', 'deleted_at',
        'status')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    date_hierarchy = 'created_at'
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostImageInline, CommentInline, CategoryInline, TagInline]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'alt', 'created_at', 'deleted_at')
    list_filter = ('created_at', 'deleted_at', ('post__created_at', JDateFieldListFilter))
    search_fields = ('post__title', 'alt')
    ordering = ('-created_at',)
    fields = ('post', 'image_file', 'alt', 'created_at', 'deleted_at')
    readonly_fields = ('created_at', 'deleted_at')
    date_hierarchy = 'created_at'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'status', 'created_at', 'is_deleted')
    list_filter = ('status', 'is_deleted', ('created_at', JDateFieldListFilter))
    search_fields = ('post__title', 'author__username', 'content')
    ordering = ('-created_at',)
    fields = ('post', 'author', 'content', 'status', 'created_at', 'is_deleted', 'deleted_at')
    readonly_fields = ('created_at', 'deleted_at')
    date_hierarchy = 'created_at'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'assigned_to', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', ('created_at', JDateFieldListFilter))
    search_fields = ('title', 'description', 'created_by__username', 'assigned_to__username')
    ordering = ('-created_at',)
    fields = ('title', 'description', 'created_by', 'assigned_to', 'status', 'priority', 'created_at')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    inlines = [TicketAttachmentInline]


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'alt', 'created_at', 'deleted_at')
    list_filter = ('created_at', 'deleted_at', ('ticket__created_at', JDateFieldListFilter))
    search_fields = ('ticket__title', 'alt')
    ordering = ('-created_at',)
    fields = ('ticket', 'file', 'alt', 'created_at', 'deleted_at')
    readonly_fields = ('created_at', 'deleted_at')
    date_hierarchy = 'created_at'


UserAdmin.inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
