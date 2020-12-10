from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from apitest.models import apiInfo, apiCase, monitorTask as monitorTaskInfo, taskResultDetail
from performanceTest.models import BusiLine
from django.views.decorators.csrf import csrf_exempt
import json
import time
import requests

import jsonpath
from django.core import serializers


# Create your views here.


def apimanage(request):
    apilist = apiInfo.objects.all()

    return render(request, 'apimanage.html', locals())


def test(request):
    # return HttpResponse(request,)
    return JsonResponse({'returncode': 200})


def editapi(request, api_id=0):
    if api_id == 0:
        busi_line = BusiLine.objects.all()
        return render(request, 'editapi.html', locals())
    else:
        busi_line = BusiLine.objects.all()
        headers = {}
        api_info = apiInfo.objects.get(api_id=api_id)
        print(api_info)

        if api_info.api_headers:
            try:
                headers = eval(api_info.api_headers)
                print(type(headers))
            except Exception as e:
                print(e)
            return render(request, 'editapi.html',
                          {"api_info": api_info, "busi_line": busi_line, "headers": headers})

        return render(request, 'editapi.html', {"api_info": api_info, "busi_line": busi_line, "headers": headers})


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
            return JsonResponse({"returncode": 201, "message": "接口名称已存在"})
        return JsonResponse({'returncode': 200, "message": "接口保存成功"})


def addapicase(request):
    if request.method == "POST":
        api_id = int(request.POST.get('path').split('/')[-2])
        print(api_id)
        busi_id = request.POST.get('busi_id')
        # 还要根据api之前录入的时候选的参数格式拿参数
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
        # 补上之前的只保存key-value对的参数，加上了额外的形式
        if len(params_dict.items()) == 0:
            params_dict = request.POST.get("apicasecontent")
        # 如果名字有重复的就认为已存在
        if not apiCase.objects.filter(apicase_name=apicase_name):
            try:
                init = apiCase.objects.create(apicase_name=apicase_name, apicase_desc=apicase_desc,
                                              apicase_express=apicase_express, apicase_except=apicase_except,
                                              apicase_params=params_dict, case_api_id=api_id, case_busi_id=busi_id)
                init.save()
            except Exception as e:
                print(e)
                return JsonResponse({'returncode': 201, 'message': '保存失败' + str(e)})
            return JsonResponse({'returncode': 200, 'message': '保存成功'})
        return JsonResponse({'returncode': 202, 'message': '保存失败,用例名称已存在'})


def addcase(request, api_id=0):
    api_id = api_id
    # api = apiInfo.objects.filter(api_id=api_id)
    # print(type(api.first()))
    # print(type(api.first().api_headers))
    busi_list = BusiLine.objects.all()
    api_info = apiInfo.objects.get(api_id=api_id)
    return render(request, 'addcase.html', locals())


def singlecase(request, api_id=0, case_id=0):
    api_id = api_id
    case_id = case_id
    # api = apiInfo.objects.filter(api_id=api_id)
    # print(type(api.first()))
    # print(type(api.first().api_headers))
    busi_list = BusiLine.objects.all()
    caseinfo = apiCase.objects.get(apicase_id=case_id)
    api_info = apiInfo.objects.get(api_id=api_id)
    params = eval(apiCase.objects.get(apicase_id=case_id).apicase_params)
    return render(request, 'addcase.html', locals())


@csrf_exempt
def singlerequest(request):
    if request.method == 'POST':
        api_name = request.POST.get("apiName")
        apicasename = request.POST.get("apicasename")
        apicasedesc = request.POST.get("apicasedesc")
        params_key = request.POST.getlist('caseparamkey')
        params_value = request.POST.getlist('caseparamvalue')
        apicase_express = request.POST.get('checkpointkey')
        apicase_except = request.POST.get('checkpointkeyvalue')
        url_path = request.POST.get('path')
        request_method = request.POST.get('method')
        returncode_expect = request.POST.get('returncode')
        params_dict = {}
        for k, v in zip(params_key, params_value):
            if k not in [None, ""] and v not in [None, ""]:
                params_dict[k] = v
        print(params_dict)
        # 根据method的不同拼凑请求方式
        # 获取请求的header
        print(apicasename)
        try:
            headers = eval(apiInfo.objects.get(api_name=api_name).api_headers)
        except Exception as e:
            print(e)
            headers = ''
        if int(request_method) == 0:
            response = requests.get(url=url_path, headers=headers, params=params_dict, )
        else:
            response = requests.post(url=url_path, headers=headers, data=params_dict)
        return_code_actual = response.status_code
        # 校验返回码
        result = ''
        header = ''
        if response.text in ['', None]:
            result = ''
        else:
            result = json.loads(response.text)  # 响应的内容转换成字典样式
            header = eval(str(response.request.headers))  # 获取的header先转换成字符串，再转为字典
        if return_code_actual == int(returncode_expect):
            # 因为如果都转换成json格式 再return 前端处理会报错，所以转字典就可以了
            result_json = json.loads(response.text)  # jsonpath处理数据必须是dict格式
            print(type(result_json))
            try:
                express_result = jsonpath.jsonpath(result_json, apicase_express)[0]
            except Exception as e:
                express_result = ''
            # json表达式获取的检查点的值和预期匹配
            if str(apicase_except) == str(express_result):
                return JsonResponse({'returncode': 200, "result": result, 'request_header': header})
            else:
                return JsonResponse({'returncode': 202, "result": result, 'request_header': header})
        else:
            return JsonResponse(
                {'returncode': 202, "result": {'returncode': return_code_actual}, 'request_header': header})


def timingTask(request):
    taskinfos = monitorTaskInfo.objects.all()
    return render(request, 'timingTask.html', locals())


def singleTaskDetail(request, task_id=0):
    task_id = task_id
    # taskinfos = monitorTaskInfo.objects.all()
    result_list = taskResultDetail.objects.filter(task_id=task_id)
    return render(request, 'singleTaskInfo.html', locals())


def monitorTask(request):
    tasks = monitorTaskInfo.objects.all()
    return render(request, 'monitorTask.html', locals())


def getcaselist(request):
    # 根据业务线查询case
    if request.method == 'GET':
        busi_id = request.GET.get('busi_id')
        print(busi_id)
        case_list_queryset = apiCase.objects.filter(case_busi_id=busi_id)
        if len(case_list_queryset) > 0:
            caseList = []
            case_format = {}
            case_list = json.loads(serializers.serialize("json", case_list_queryset))
            print(case_list)
            for case in case_list:
                caseList.append({
                    "importUnitId": str(case['pk']),
                    "importUnitName": case['fields']['apicase_name'],
                    "flag": 'false',
                })
            return JsonResponse({'caseList': caseList})
        else:
            return JsonResponse({'caseList': []})


def getdata(request):
    #  data = json.dumps({"data": [{"name1", "name2", "name3", "name4", "name5", "name6", "name7"}]})
    data1 = [{"busi": "name7", "name": "name1", "casecount": "name2", "tasktype": "name3", "savetime": "name4",
              "result": "name5", "action": "name6"}]

    data2 = {"data": [{"busi": "name7", "name": "name1", "casecount": "name2", "tasktype": "name3",
                       "savetime": "namsssssssssssssssssssssssssssse4",
                       "result": "7 | 1", "action": "name6"},
                      {"busi": "name7", "name": "name1", "casecount": "name2", "tasktype": "name3",
                       "savetime": "name4",
                       "result": "name5", "action": "bbbbbbbbb"},
                      {"busi": "name7", "name": "name1", "casecount": "name2", "tasktype": "name3",
                       "savetime": "name4",
                       "result": "name5", "action": "name6"},
                      {"busi": "name7", "name": "name1", "casecount": "name2", "tasktype": "name3",
                       "savetime": "name4",
                       "result": "5 | 1", "action": "name6"}, ]}
    # 如果是ajax过来请求数据 需要对queryset的数据做序列化然后针对外键还有做特殊处理很麻烦
    task = {}
    tasks_list = []
    if len(monitorTaskInfo.objects.all()) > 0:
        queryset_tasks = json.loads(serializers.serialize("json", monitorTaskInfo.objects.all()))
        busi_dict = BusiLine.objects.values('busi_id', 'busi_name')
        print(busi_dict)
        print(queryset_tasks)
        busi_actual = {}
        task_type = {
            0: "自动",
            1: "手动"
        }
        for busi in busi_dict:
            busi_actual[busi['busi_id']] = busi['busi_name']
        print(busi_actual)
        for task in queryset_tasks:
            tasks_list.append({
                "busi": busi_actual[task['fields']['monitorTask_busi']],
                "name": task['fields']['monitorTask_name'],
                "casecount": len(task['fields']['monitorTask_caseList']),
                "type": task_type[task['fields']['monitorTask_type']],
                "savetime": task['fields']['monitorTask_c_time'],

            })
        print(queryset_tasks)
        print(tasks_list)

    print(type(data2))
    # return JsonResponse(data2)
    return HttpResponse(json.dumps(data2))


@csrf_exempt
def addMonitorCase(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        busi_id = request.POST.get('busi_id')
        type_task = request.POST.get('typeOfTask')
        cron_time = request.POST.get('cron_time')
        case_list = request.POST.get('case_list')
        if not monitorTaskInfo.objects.filter(monitorTask_name=task_name):
            try:
                init = monitorTaskInfo.objects.create(monitorTask_name=task_name, monitorTask_busi_id=busi_id,
                                                      monitorTask_type=type_task, monitorTask_caseList=case_list,
                                                      monitorTask_cron=cron_time)
                init.save()
                return JsonResponse({'returncode': 200, 'message': '保存成功'})
            except Exception as e:
                print(e)
                return JsonResponse({'returncode': 201, 'message': '保存失败,{0}'.format(e)})
        return JsonResponse({'returncode': 202, 'message': '任务已存在，请修改后提交'})


from threading import Thread


def async_task(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def manualExecTask(request):
    if request.method == 'GET':
        task_name = request.GET.get('task_name')
        print(task_name)
        taskexec_id = monitorTaskInfo.objects.get(monitorTask_name=task_name).monitorTask_id
        # 根据task_name获取task下的case_list
        case_list = eval(monitorTaskInfo.objects.get(monitorTask_name=task_name).monitorTask_caseList.replace("true",
                                                                                                              "\'true\'").replace(
            "false", "\'false\'"))
        print(case_list, taskexec_id)
        # 这些拼装数据的操作都需要后期 缓存到redis或者使用kafka
        sendRequestAsync(case_list, taskexec_id)

        return JsonResponse({'returncode': 200})


@async_task
def sendRequestAsync(case_list, taskexec_id):
    startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    resp_success_list = []
    resp_failure_list = []
    for case in case_list:
        case_id = int(case["importUnitId"])
        print(case_id)
        # 根据case_id_list拼装request_list 要遍历case_id_list然后拼装
        api_case = apiCase.objects.get(apicase_id=case_id)
        api_id = api_case.case_api_id
        api_info = apiInfo.objects.get(api_id=api_id)
        api_type = api_info.api_type  # 获取此case是get还是post
        api_url = api_info.api_url  # 获取此case的请求url
        headers = eval(api_info.api_headers)  # 获取请求头
        data = eval(api_case.apicase_params)
        # print(case_id, api_id, api_type, api_url, type(headers), type(data))
        # 下面是grequests的处理代码
        #     if api_type == 0:
        #         req_list.append(grequests.get(api_url, headers=headers, params=data))
        #     else:
        #         req_list.append(grequests.post(api_url, headers=headers, data=data))
        #     print(req_list)
        # resq =  grequests.map(req_list)
        # print(resq)
        # for item in resq:
        #     print(item.status_code,item.request.headers,item.text)
        if api_type == 0:
            try:
                resp = requests.get(url=api_url, headers=headers, params=data)
                # 先判断返回码是否符合
                if int(resp.status_code) == int(api_case.apicase_returncode):
                    try:
                        result_json = json.loads(resp.text)
                        express_result = jsonpath.jsonpath(result_json, api_case.apicase_express)[0]
                        if str(express_result) == str(api_case.apicase_except):
                            resp_success_list.append(
                                {'case_id': case_id, 'status_code': resp.status_code, 'resp_content': resp.text,
                                 'header': resp.request.headers})
                        else:
                            resp_failure_list.append(
                                {'case_id': case_id, 'status_code': resp.status_code, 'resp_content': resp.text,
                                 'header': resp.request.headers, 'failue': 'expectResultFalse'})
                    except Exception as e:
                        resp_failure_list.append(
                            {'case_id': case_id, 'status_code': '', 'resp_content': '',
                             'header': '', 'error': e})
                else:
                    resp_failure_list.append({'case_id': case_id, 'status_code': '', 'resp_content': '',
                                              'header': '', 'failue': 'returncode'})
            except Exception as e:
                resp_failure_list.append({'case_id': case_id, 'status_code': '', 'resp_content': '',
                                          'header': '', 'error': e})
        else:
            try:
                resp = requests.post(url=api_url, headers=headers, data=data, verify=False)
                # 先判断返回码是否符合
                if int(resp.status_code) == int(api_case.apicase_returncode):
                    try:
                        result_json = json.loads(resp.text)
                        express_result = jsonpath.jsonpath(result_json, api_case.apicase_express)[0]
                        if str(express_result) == str(api_case.apicase_except):
                            resp_success_list.append(
                                {'case_id': case_id, 'status_code': resp.status_code, 'resp_content': resp.text,
                                 'header': resp.request.headers})
                    except Exception as e:
                        resp_failure_list.append(
                            {'case_id': case_id, 'status_code': '', 'resp_content': '',
                             'header': '', 'error': e})
                else:
                    resp_failure_list.append({'case_id': case_id, 'status_code': '', 'resp_content': '',
                                              'header': '', 'failue': 'returncode'})
            except Exception as e:
                resp_failure_list.append({'case_id': case_id, 'status_code': '', 'resp_content': '',
                                          'header': '', 'error': e})

    endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    try:
        init = taskResultDetail.objects.create(task_id=taskexec_id, taskResult_success=resp_success_list,
                                               taskResult_failure=resp_failure_list, taskexec_startTime=startTime,
                                               taskexec_endTime=endTime)
        init.save()
    except Exception as e:
        print(e)
