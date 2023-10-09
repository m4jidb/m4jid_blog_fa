import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from taggit.forms import TagWidget
from .models import Profile, Post, PostImage, Comment, Ticket, TicketAttachment
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=200, required=True, label='نام')
    last_name = forms.CharField(max_length=200, required=True, label='نام خانوادگی')
    phone = forms.CharField(max_length=20, required=True, label='شماره تلفن')
    email = forms.EmailField(required=True, label='ایمیل')

    error_messages = {
        'invalid_username': 'نام کاربری می‌تواند شامل حروف، اعداد و نمادهای @/./+/-/_ باشد.',
        'long_username': 'نام کاربری نمی‌تواند بیش از 150 کاراکتر داشته باشد.',
        'invalid_phone': 'شماره تلفن نامعتبر. باید 11 رقمی باشد که با 0 شروع شود یا با کد کشور و سپس شماره تلفن شروع شود.',
        'password_mismatch': 'دو قسمت رمز عبور مطابقت نداشتند.',
        'email_exists': 'این ایمیل از قبل ثبت شده است. لطفا از ایمیل دیگری استفاده کنید.',
        'phone_exists': 'این شماره تلفن از قبل ثبت شده است. لطفا از شماره تلفن دیگری استفاده کنید.',
    }

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone', 'email', 'password1', 'password2']
        labels = {
            'username': 'نام کاربری',
            'password1': 'گذرواژه',
            'password2': 'تکرار گذرواژه',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 150:
            raise ValidationError(self.error_messages['long_username'])
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError(self.error_messages['invalid_username'])
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not re.match(r'^(0\d{10}|\+\d{1,3}\d{10})$', phone):
                raise ValidationError(self.error_messages['invalid_phone'])
            if User.objects.filter(profile_user__phone=phone).exists():
                raise ValidationError(self.error_messages['phone_exists'])
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(self.error_messages['email_exists'])
        return email

    def clean(self):
        super().clean()
        try:
            self.clean_phone()
            self.clean_email()
        except forms.ValidationError as e:
            self.add_error('phone', e)
            self.add_error('email', e)

    def save(self, commit=True):
        user = super().save(commit=False)
        phone = self.cleaned_data.get('phone')
        if commit:
            user.save()
            Profile.objects.create(user=user, phone=phone)
        return user


class LogInForm(forms.Form):

    username = forms.CharField(label='نام کاربری یا شماره تلفن', max_length=150)
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)


class UsernameEditForm(forms.ModelForm):

    new_username = forms.CharField(label='New Username', max_length=150)

    class Meta:
        model = User
        fields = ['new_username']

    def clean_new_username(self):
        new_username = self.cleaned_data['new_username']
        if User.objects.filter(username=new_username).exists():
            raise ValidationError('این نام کاربری از قبل انتخاب شده است. لطفا یکی دیگر را انتخاب کنید.')
        return new_username


class FirstNameEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name']


class LastNameEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name']


class EmailEditForm(forms.ModelForm):

    error_messages = {
        'email_exists': 'این ایمیل از قبل ثبت شده است. لطفا از ایمیل دیگری استفاده کنید.',
    }

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(self.error_messages['email_exists'])
        return email


class CodeVerificationForm(forms.Form):
    code = forms.IntegerField(
        label='کد تایید',
        widget=forms.TextInput(attrs={'placeholder': 'لطفاً کد تایید را وارد کنید'}),
        error_messages={
            'required': 'وارد کردن کد تایید الزامی است.',
            'invalid': 'لطفاً یک عدد معتبر وارد کنید.',
        }
    )


class PhoneEditForm(forms.ModelForm):

    error_messages = {
        'invalid_phone': 'شماره تلفن نامعتبر. باید 11 رقمی باشد که با 0 شروع شود یا با کد کشور و سپس شماره تلفن شروع شود.',
        'phone_exists': 'این شماره تلفن از قبل ثبت شده است. لطفا از شماره تلفن دیگری استفاده کنید.',
    }

    class Meta:
        model = Profile
        fields = ['phone']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not re.match(r'^(0\d{10}|\+\d{1,3}\d{10})$', phone):
                raise ValidationError(self.error_messages['invalid_phone'])
            if User.objects.filter(profile_user__phone=phone).exists():
                raise ValidationError(self.error_messages['phone_exists'])
        return phone


class BirthdayEditForm(forms.ModelForm):

    birthday = JalaliDateField(widget=AdminJalaliDateWidget, label='تاریخ تولد')

    class Meta:
        model = Profile
        fields = ['birthday']


class AddressEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['address']


class CityEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['city']


class StateEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['state']


class CountryEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['country']


class PostCreateForm(forms.ModelForm):
    tags = forms.CharField(label='برچسب ها', required=False, widget=TagWidget())
    categories = forms.CharField(label='دسته بندی ها', required=False, widget=TagWidget())

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'categories']


class PostImageForm(forms.ModelForm):
    image_file = forms.ImageField(label='تصویر پست')

    class Meta:
        model = PostImage
        fields = ['image_file']


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'categories']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'content']


class TicketAttachmentForm(forms.ModelForm):
    class Meta:
        model = TicketAttachment
        fields = ['file', 'alt']
