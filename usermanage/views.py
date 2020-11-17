from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import form
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
import random, os
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django


def scripttest(request):
    return render(request, 'login/scripttest.html')


def getCpuLoad(request):
    data = {
        'data': [10000, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 60000]}
    print(1)
    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def test(request):
    if request.method == "POST":
        print(request.session.keys())
        print(request.session.values())
        return HttpResponse({"RESULT": "TEST"})


@csrf_exempt
def saveFile(request):
    if request.method == 'POST':
        testFile = request.FILES.get("myfile", None)
        print(request.session.keys())
        print(request.session.values())
        print(request.session.get('user_name'))
        if not testFile:
            return HttpResponse("NO FILE FOR UPLOAD")
        with open(os.path.join(r"D:\files", testFile.name), 'wb+') as f:
            for chunk in testFile.chunks():
                f.write(chunk)
            data = {
                "result": "UPLOAD SUCESS"
            }

            return HttpResponse(json.dumps(data), content_type="application/json")


# html版本
# def login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         print(username, password)
#         if username.strip() and password:
#             try:
#                 user = models.User.objects.get(name=username)
#                 print(user)
#             except Exception as e:
#                 message = '用户不存在'
#                 return render(request, 'login/login_old.html',{'message':message})
#             if user.password == password:
#                 return redirect('/index/')
#             else:
#                 message = '密码不正确'
#                 return render(request,'login/login_old.html',{'message':message})
#
#     return render(request, 'login/login_old.html')

# django form 表单版本
@csrf_exempt
def login(request):
    if request.session.get('is_login', None):
        return redirect('/dashboard/')
    if request.method == "POST":

        username = request.POST.get('username')
        if not username:
            return render(request, 'login/login.html')
        password = request.POST.get('password')
        try:
            user = models.User.objects.get(name=username)
        except:
            message = '用户名不存在'
            return render(request, 'login/login.html', locals())
        if user.password == password:
            # request.session虽然设置了session的key和value，然而这个操作并没有在django那认为你已经登陆了
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            user = authenticate(username=username, password=password)
            login_django(request, user)  # django 自带的登录，将验证通过的用户保存在request request.user
            return redirect('/dashboard/')
        else:
            message = '密码不正确'
            return render(request, 'login/login.html', locals())
    else:
        return render(request, 'login/login.html', locals())


"""
@csrf_exempt
def login(request):
    if request.session.get('is_login', None):
        return redirect('/dashboard/')
    if request.method == "POST":
        next_url = request.POST.get("next","/dashboard")
        login_form = form.UserForm(request.POST)
        message = '请检查输入的内容'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '不存在'
                return render(request, 'login/login.html', locals())
            if user.password == password:
                # request.session虽然设置了session的key和value，然而这个操作并没有在django那认为你已经登陆了
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                user = authenticate(username=username, password=password)
                login_django(request, user)  # django 自带的登录，将验证通过的用户保存在request request.user
                return redirect(next_url)
            else:
                message = '密码不正确'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = form.UserForm
    return render(request, 'login/login.html', locals())

"""


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == "POST":
        register_form = form.RegisterForm(request.POST)
        message = '请检查输入的内容'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            if password1 != password2:
                message = '两次输入密码不一致'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user == username:
                    message = '用户名已存在'
                    return render(request, 'login/register.html', locals())
                same_name_email = models.User.objects.filter(email=email)
                if same_name_email == email:
                    message = '邮箱已注册'
                    return render(request, 'login/register.html', locals())
                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = form.RegisterForm()

    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")
