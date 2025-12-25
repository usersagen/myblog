
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='register'),
    path('captcha',views.captcha,name='captcha'),
    path('index',views.index,name='index'),
]