from .forms import UserSignUpForm
from django.shortcuts import render, redirect
from django.contrib import messages


def user_sign_up_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'حساب با موفقیت برای {username} ساخته شد .')
            return redirect('blog:index')
    else:
        form = UserSignUpForm()

    return render(request, 'accounts/user_sign_up.html', {'form': form})


def index(request):
    ...
    return render(request, 'blog/index.html')
