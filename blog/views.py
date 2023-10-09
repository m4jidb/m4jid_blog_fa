from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.utils.text import slugify
from django.forms import inlineformset_factory
from .forms import (
    SignUpForm, LogInForm, FirstNameEditForm, LastNameEditForm, BirthdayEditForm, AddressEditForm, CityEditForm,
    StateEditForm, CountryEditForm, UsernameEditForm, PhoneEditForm, CodeVerificationForm, PostCreateForm,
    EmailEditForm, PostEditForm, PostImageForm, CommentForm, TicketForm, TicketAttachmentForm
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
from .models import Post, PostImage, TicketAttachment, Ticket


def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:log_in')
    else:
        form = SignUpForm()
    return render(request, 'accounts/sign_up.html', {'form': form})


def log_in_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog:index')
        else:
            return HttpResponse('نام کاربری یا رمز عبور نامعتبر است.')
    else:
        form = LogInForm()
        return render(request, 'accounts/log_in.html', {'form': form})


@login_required
def check_out_view(request):
    return render(request, 'accounts/check_out.html')


@login_required
def log_out_view(request):
    logout(request)
    return redirect('blog:loged_out')


def loged_out_view(request):
    return render(request, 'accounts/loged_out.html')


@login_required
def profile_view(request):
    user = request.user
    profile = user.profile_user

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def user_account_information_view(request):
    return render(request, 'accounts/user_account_information.html')


@login_required
def user_post_list_view(request):
    user_posts = Post.objects.filter(author=request.user)
    paginator = Paginator(user_posts, 1)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {'posts': posts}
    return render(request, 'accounts/user_post_list.html', context)


@login_required
def user_ticket_list_view(request):
    user_tickets = Ticket.objects.filter(created_by=request.user)
    paginator = Paginator(user_tickets, 2)
    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number)
    context = {'tickets': tickets}
    return render(request, 'accounts/user_ticket_list.html', context)


@login_required
def username_edit_view(request):
    if request.method == 'POST':
        form = UsernameEditForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['new_username']
            user.save()
            messages.success(request, 'نام کاربری شما با موفقیت به روز شد.')
            return redirect('blog:profile')
    else:
        form = UsernameEditForm(instance=request.user)

    return render(request, 'accounts/username_edit.html', {'form': form})


@login_required
def first_name_edit_view(request):
    if request.method == 'POST':
        form = FirstNameEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'نام خانوادگی شما با موفقیت به روز شد.')
            return redirect('blog:profile')
    else:
        form = FirstNameEditForm(instance=request.user)

    return render(request, 'accounts/first_name_edit.html', {'form': form})


@login_required
def last_name_edit_view(request):
    if request.method == 'POST':
        form = LastNameEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'نام شما با موفقیت به روز شد.')
            return redirect('blog:profile')
    else:
        form = LastNameEditForm(instance=request.user)

    return render(request, 'accounts/last_name_edit.html', {'form': form})


@login_required
def email_edit_view(request):
    if request.method == 'POST':
        form = EmailEditForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data.get('email')
            code = random.randint(100000, 999999)
            request.session['code'] = code
            request.session['new_email'] = new_email
            send_mail(
                'تایید تغییر ایمیل',
                f'کد تایید شما {code} است.',
                'm4jidb@gmail.com',
                [new_email],
                fail_silently=False,
            )
            return redirect('blog:verify_code')
    else:
        form = EmailEditForm()
    return render(request, 'accounts/email_edit.html', {'form': form})


def verify_code_view(request):
    stored_code = request.session.get('code')

    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)

        if form.is_valid():
            entered_code = form.cleaned_data['code']

            if stored_code == entered_code:
                new_email = request.session.get('new_email')
                user = request.user
                user.email = new_email
                user.save()

                del request.session['code']
                del request.session['new_email']

                messages.success(request, 'تغییر ایمیل با موفقیت انجام شد.')
                return redirect('blog:profile')
            else:
                messages.error(request, 'کد وارد شده اشتباه است. لطفاً دقت کنید.')

    else:
        form = CodeVerificationForm()

    return render(request, 'accounts/verify_code.html', {'form': form})


@login_required
def phone_edit_view(request):
    if request.method == 'POST':
        form = PhoneEditForm(request.POST, instance=request.user.profile_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'شماره تلفن شما با موفقیت به روز شد.')
            return redirect('blog:profile')
    else:
        form = PhoneEditForm(instance=request.user)

    return render(request, 'accounts/phone_edit.html', {'form': form})


@login_required
def birthday_edit_view(request):
    if request.method == 'POST':
        form = BirthdayEditForm(request.POST, instance=request.user.profile_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تاریخ تولد شما با موفقیت به روز شد.')
            return redirect('blog:profile')
    else:
        form = BirthdayEditForm(instance=request.user)

    return render(request, 'accounts/birthday_edit.html', {'form': form})


@login_required
def address_edit_view(request):
    if request.method == 'POST':
        form = AddressEditForm(request.POST, instance=request.user.profile_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'آدرس شما با موفقیت به روز شد.')
            return redirect('blog:profile')
    else:
        form = AddressEditForm(instance=request.user)

    return render(request, 'accounts/address_edit.html', {'form': form})


@login_required
def city_edit_view(request):
    if request.method == 'POST':
        form = CityEditForm(request.POST, instance=request.user.profile_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'شهر شما با موفقیت به روز شد.')
            return redirect('blog:profile')
    else:
        form = CityEditForm(instance=request.user)

    return render(request, 'accounts/city_edit.html', {'form': form})


@login_required
def state_edit_view(request):
    if request.method == 'POST':
        form = StateEditForm(request.POST, instance=request.user.profile_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'استان شما با موفقیت به روز شد.')
            return redirect('blog:profile')
    else:
        form = StateEditForm(instance=request.user)

    return render(request, 'accounts/state_edit.html', {'form': form})


@login_required
def country_edit_view(request):
    if request.method == 'POST':
        form = CountryEditForm(request.POST, instance=request.user.profile_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'کشور شما با موفقیت به روز شد.')
            return redirect('blog:profile')
    else:
        form = CountryEditForm(instance=request.user)

    return render(request, 'accounts/country_edit.html', {'form': form})


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('blog:password_change_done')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})


@login_required
def password_change_done_view(request):
    return render(request, 'accounts/password_change_done.html')


@login_required
def post_create_view(request):
    image_form_set = modelformset_factory(PostImage, form=PostImageForm, extra=10)
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        formset = image_form_set(request.POST, request.FILES, queryset=PostImage.objects.none())
        if form.is_valid() and formset.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user

            new_post.slug = slugify(new_post.title)
            orig_slug = new_post.slug
            counter = 1

            while Post.objects.filter(slug=new_post.slug).exists():
                new_post.slug = '%s-%s' % (orig_slug, counter)
                counter += 1

            new_post.save()
            tags = form.cleaned_data['tags']
            categories = form.cleaned_data['categories']
            new_post.tags.set(*tags.split(','))
            new_post.categories.set(*categories.split(','))

            for image_form in formset:
                image = image_form.save(commit=False)
                image.post = new_post
                image.save()

            return redirect('blog:index')

    else:
        form = PostCreateForm()
        formset = image_form_set(queryset=PostImage.objects.none())

    return render(request, 'forms/post_create.html', {'form': form, 'formset': formset})


def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_edit_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post_image_form_set = inlineformset_factory(Post, PostImage, form=PostImageForm, extra=1)

    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        formset = post_image_form_set(request.POST, request.FILES, instance=post)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostEditForm(instance=post)
        formset = post_image_form_set(instance=post)

    context = {'form': form, 'formset': formset, 'post': post}
    return render(request, 'forms/post_edit.html', context)


def index_view(request):
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 1)  # Show 10 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


@login_required
def comment_add_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'forms/comment_add.html', {'form': form})


@login_required
def ticket_create_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        file_form = TicketAttachmentForm(request.POST, request.FILES)
        if form.is_valid() and file_form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()

            TicketAttachment.objects.create(
                file=file_form.cleaned_data['file'],
                alt=file_form.cleaned_data['alt'],
                ticket=ticket
            )
            return redirect('blog:user_ticket_list')
    else:
        form = TicketForm()
        file_form = TicketAttachmentForm()
    return render(request, 'forms/ticket.html', {'form': form, 'file_form': file_form})


@login_required
def ticket_detail_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'accounts/ticket_detail.html', {'ticket': ticket})
