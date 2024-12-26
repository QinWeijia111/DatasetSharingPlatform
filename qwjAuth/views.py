from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.core.mail import send_mail
from .models import CaptchaModel
import string
import random
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout

User = get_user_model()


# Create your views here.
@require_http_methods(['GET', 'POST'])
def qwjlogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            user = User.objects.get(email=email)
            if user and user.check_password(password):
                login(request, user)
                if not remember_me:
                    # 如果没有选中记住我，将不会将信息保存在session中
                    request.session.set_expiry(0)
                # 如果点击了记住我，信息将默认在session中保存两周
                return redirect('/')
            else:
                print("邮箱或者密码错误")
                return redirect(reverse('qwjAuth:login'))


def qwjlogout(request):
    logout(request)
    return redirect('/')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse("qwjAuth:login"))
        else:
            print(form.errors)
            return redirect(reverse("qwjAuth:register"))


def send_eamil_captcha(request):
    # 前端发送的邮箱url格式应该是 ?email = xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'msg': '邮箱发送失败'})
    # 随机生成四位的验证码
    captcha = "".join(random.sample(string.digits, 4))
    # 将生成的随机数存储到数据库CaptchaModel中
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail("秦维嘉数据集共享平台验证码", f"您的验证码是{captcha}", from_email=None, recipient_list=[email])
    return JsonResponse({'code': 200, 'msg': '邮箱验证码发送成功'})
