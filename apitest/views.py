from django.shortcuts import render
from django.http import JsonResponse
from apitest.models import apiInfo, apiCase
from performanceTest.models import BusiLine
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.


def apimanage(request):
    apilist = apiInfo.objects.all()

    return render(request, 'apimanage.html', locals())


def editapi(request, api_id=0):
    if api_id == 0:
        busi_line = BusiLine.objects.all()
        return render(request, 'editapi.html', locals())
    else:
        busi_line = BusiLine.objects.all()
        try:
            api_info = apiInfo.objects.get(api_id=api_id)
            print(api_info)
            headers = {}

            if api_info.api_headers:
                try:
                    headers = eval(api_info.api_headers)
                    print(type(headers))
                except Exception as e:
                    print(e)
                return render(request, 'editapi.html',
                              {"api_info": api_info, "busi_line": busi_line, "headers": headers})
        except:
            return render(request, 'editapi.html', locals())


def apicase(request):
    apicases = apiCase.objects.all()
    return render(request, 'apicase.html', locals())


@csrf_exempt
def saveapi(request):
    if request.method == "POST":
        apiname = request.POST.get("apiname")
        header_key = request.POST.getlist("headerkey")
        header_value = request.POST.getlist("headervalue")
        api_busi = request.POST.get("busi")
        apiurl = request.POST.get("apiurl")
        apidesc = request.POST.get("apidesc")
        method = request.POST.get("method")
        contenttype = request.POST.get("contenttype")
        apicontent = request.POST.get("apicontent")

        # param_zip = zip([a for a in key if a is not ""], [b for b in value if b is not ""])
        if not apiInfo.objects.filter(api_name=apiname):
            header_dict = {}
            for k, v in zip(header_key, header_value):
                if k not in [None, ""] and v not in [None, ""]:
                    header_dict[k] = v
            print(header_dict)
            s = apiInfo.objects.create(api_name=apiname, api_url=apiurl, api_busi_id=int(api_busi), api_type=method,
                                       api_contenttype=int(contenttype), api_content=apicontent, api_apidesc=apidesc,
                                       api_headers=header_dict)
            s.save()
        else:
            return JsonResponse({"returncode": 200, "message": "接口名称已存在"})
        return JsonResponse({'returncode': 200, "message": "接口保存成功"})


@csrf_exempt
def saveapicase(request):
    if request.method == "POST":
        api_id = int(request.POST.get('path').split('/')[-2])
        print(api_id)
        # 还要根据api之前录入的时候选的参数格式
        apicase_name = request.POST.get('apicasename')
        apicase_desc = request.POST.get('apicasedesc')
        apicase_express = request.POST.get('checkpointkey')
        apicase_except = request.POST.get('checkpointkeyvalue')
        params_key = request.POST.getlist('caseparamkey')
        params_value = request.POST.getlist('caseparamvalue')
        params_dict = {}
        for k, v in zip(params_key, params_value):
            if k not in [None, ""] and v not in [None, ""]:
                params_dict[k] = v
        print(params_dict)
        # 如果名字有重复的就认为已存在
        if not apiCase.objects.filter(apicase_name=apicase_name):
            try:
                init = apiCase.objects.create(apicase_name=apicase_name, apicase_desc=apicase_desc,
                                              apicase_express=apicase_express, apicase_except=apicase_except,
                                              apicase_params=params_dict, case_api_id_id=api_id)
                init.save()
            except Exception as e:
                print(e)
                return JsonResponse({'returncode': 201, 'message': '保存失败'})
            return JsonResponse({'returncode': 200, 'message': '保存成功'})


def addcase(request, api_id=0):
    api_id = api_id
    # api = apiInfo.objects.filter(api_id=api_id)
    # print(type(api.first()))
    # print(type(api.first().api_headers))
    busi_list = BusiLine.objects.all()
    api_info = apiInfo.objects.get(api_id=api_id)
    return render(request, 'addcase.html', locals())


@csrf_exempt
def singlerequest(request):
    if request.method == 'POST':
        apicasename = request.POST.get("apiname")
        apicasedesc = request.POST.get("apicasedesc")
        print(apicasename, apicasedesc)
        return JsonResponse({'returncode': 200})
