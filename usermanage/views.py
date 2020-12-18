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


def plateDataSumary(request):
    return render(request, 'login/plateDataSumary.html')


def getCpuLoad(request):
    data = {
        'data': [134, 87, 65, 232, 133, 140, 180, 244, 267, 312, 278, 216]}
    print(1)
    return HttpResponse(json.dumps(data), content_type="application/json")


def datasumary(request):
    if request.method == 'GET':
        data = {"apidata":
            {
                "all": 5007,
                "charts": {
                    "家": 237,
                    "产品库": 264,
                    "论坛": 561,
                    "车主价格": 778,
                    "小视频": 355,
                    "关注": 405,
                    "轻应用": 842,
                    "小程序": 290,
                    "本地化": 762,
                    "二手车": 593,
                    "818晚会": 260,
                    "付费会员": 537,
                    "资讯": 408,
                    "直播": 607,
                    "创客云": 192,
                    "车友圈": 168
                },
                "components": {
                    "家": 1788,
                    "产品库": 2575,
                    "论坛": 2400,
                    "车主价格": 3342,
                    "小视频": 3425,
                    "关注": 4055,
                    "轻应用": 2392,
                    "小程序": 2347,
                    "本地化": 1882,
                    "二手车": 3875,
                    "818晚会": 3879,
                    "付费会员": 1537,
                    "资讯": 897,
                    "直播": 1800,
                    "创客云": 563,
                    "车友圈": 782
                },
                "ie": 9743
            },
            "taskdatasumary": {
                "大数据部": 30,
                "技术中台部": 21,
                "技术前台部": 45,
                "人力部": 60,

            },
            "alermtasksumary": {
                "家家小秘": 64,
                "二手车": 15,
                "资讯": 18,
                "车友圈": 11,
                "关注": 29,
                "直播": 72
            }
        }

        return JsonResponse({'data': data})


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
