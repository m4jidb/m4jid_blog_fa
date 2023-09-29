from django.urls import path
from . import views


app_name = "blog"


urlpatterns = [
    path('sign-up/', views.user_sign_up_view,  name='user_sign_up'),
    path('index/', views.index, name='index'),
]
