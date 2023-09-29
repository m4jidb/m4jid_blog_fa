from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=200, required=True, label='نام')
    last_name = forms.CharField(max_length=200, required=True, label='نام خانوادگی')
    phone_number = forms.CharField(max_length=11, required=True, label='شماره تلفن')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone_number', 'password1', 'password2']
        labels = {
            'username': 'نام کاربری',
            'password1': 'گذرواژه',
            'password2': 'تکرار گذرواژه',
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('شماره تلفن الزامی است.')
        if not phone_number.isdigit():
            raise forms.ValidationError('شماره تلفن باید فقط شامل ارقام باشد.')
        elif len(phone_number) != 11:
            raise forms.ValidationError('شماره تلفن باید دقیقاً 11 رقم باشد.')
        elif not phone_number.startswith('0'):
            raise forms.ValidationError('شماره تلفن باید با 0 شروع شود.')
        return phone_number

    def clean(self):
        super().clean()

        try:
            self.clean_phone_number()
        except forms.ValidationError as e:
            self.add_error('phone_number', e)
