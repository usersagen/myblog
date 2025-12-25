from django.shortcuts import render, redirect, reverse,HttpResponse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required


User = get_user_model()

@login_required(login_url='login')
def index(request):
    return HttpResponse("登录成功")

# 登录
@require_http_methods(['GET','POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data.get('remember',False)

            user = auth.authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                auth.login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                messages.success(request, '登录成功')
                next_url = request.GET.get('next') or 'user:index'   # 预留接口 登录成功要跳转的页面
                return redirect(next_url)
            else:
                messages.error(request, '用户名或密码错误')
    return render(request, 'login.html', {"form": form})

# 退出账号
def logout(request):
    username = request.user.username
    auth.logout(request)
    messages.success(request, f'{username}退出成功')
    print(f'{username}退出成功')
    return redirect('user:login')

# 注册
@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(email=email, username=username, password=password)
            messages.success(request, f'{username}注册成功')
            print("注册成功")
            return redirect('user:login')
        else:
            messages.error(request, '注册失败，请检查！')
            print(form.errors)
            return render(request, 'register.html', {"form": form})

# 发送验证码
def captcha(request):
    email = request.GET.get('email')
    if not email:
        messages.error(request, '邮箱为空！')
        return JsonResponse({"code": 400, "message": '必须传递邮箱！'})
    captcha = ''.join(random.sample(string.digits, 4))  # 生成验证码
    CaptchaModel.objects.update_or_create(email=email,captcha=captcha)  # 存储到数据库
    send_mail("注册验证码",message=f"您的验证码是：{captcha}",recipient_list=[email],from_email=None)   # 发送验证码
    messages.success(request, '验证码发送成功！')
    return JsonResponse({"code": 200, "message": '验证码发送成功！'})
