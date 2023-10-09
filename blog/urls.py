from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


app_name = "blog"


urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign_up'),
    path('log-in/', views.log_in_view, name='log_in'),
    path('check-out/', views.check_out_view, name='check_out'),
    path('log-out/', views.log_out_view, name='log_out'),
    path('loged-out/', views.loged_out_view, name='loged_out'),
    path('profile/', views.profile_view, name='profile'),
    path('user-account-information/', views.user_account_information_view, name='user_account_information'),
    path('user-post-list/', views.user_post_list_view, name='user_post_list'),
    path('user-ticket-list/', views.user_ticket_list_view, name='user_ticket_list'),
    path('username-edit/', views.username_edit_view, name='username_edit'),
    path('first-name-edit/', views.first_name_edit_view, name='first_name_edit'),
    path('last-name-edit/', views.last_name_edit_view, name='last_name_edit'),
    path('email-edit/', views.email_edit_view, name='email_edit'),
    path('verify-code/', views.verify_code_view, name='verify_code'),
    path('phone-edit/', views.phone_edit_view, name='phone_edit'),
    path('date-of-birth-edit/', views.birthday_edit_view, name='date_of_birth_edit'),
    path('address-edit/', views.address_edit_view, name='address_edit'),
    path('city-edit/', views.city_edit_view, name='city_edit'),
    path('state-edit/', views.state_edit_view, name='state_edit'),
    path('country-edit/', views.country_edit_view, name='country_edit'),
    path('password-change/', views.password_change_view, name='password_change'),
    path('password-change-done/', views.password_change_done_view, name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        subject_template_name='accounts/password_reset_subject.txt',
        email_template_name='accounts/password_reset_email.html',
        success_url=reverse_lazy('blog:password_reset_done'),
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html',
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('blog:password_reset_complete'),
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html',
    ), name='password_reset_complete'),
    path('index/', views.index_view, name='index'),
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit_view, name='post_edit'),
    path('post-create/', views.post_create_view, name='post_create'),
    path('post/<slug:slug>/add-comment/', views.comment_add_view, name='comment_add'),
    path('ticket', views.ticket_create_view, name='ticket_create'),
    path('ticket/<int:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
]
