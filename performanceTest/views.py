from django.shortcuts import render
from django.db import models
from .models import TaskList
from .models import TaskList, ServerInfo, BusiLine
from django.core import serializers
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
import random


# Create your views here.

@login_required(login_url='/login/')
def firstpage(request):
    num = len(ServerInfo.objects.all())

    print(request.session.get('is_login'))
    unusecount = len(ServerInfo.objects.filter(server_status=0))
    taskcount = len(TaskList.objects.all())
    short = ['All thing in their being are good for something.',
             'The good seaman is known in bad weather.',
             'Cease to struggle and you cease to live.'][random.randint(0, 2)]
    data = json.dumps([10000, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 60000])
    print(data)
    return render(request, 'login/dashboard.html', locals())


def performance(request):
    return render(request, 'performance/performance.html')


def getServerCount(request):
    try:
        huaweiCloud = len(ServerInfo.objects.filter(server_cloud="huaweiCloud"))
        tencentCloud = len(ServerInfo.objects.filter(server_cloud="tencentCloud"))
        aliCloud = len(ServerInfo.objects.filter(server_cloud="aliCloud"))
        data = [huaweiCloud, tencentCloud, aliCloud]
    except Exception as e:
        return JsonResponse({'returncode': 500, 'message': e})
    return JsonResponse({'returncode': 200, 'data': data})


@login_required
def tasklist(request):
    # data_from_db = TaskList.objects.all()
    # data = json.loads(serializers.serialize("json", data_from_db)) 序列化
    # print(type(data))
    # print(data)
    # datalist = []
    # for task in data:
    #     tasks = task['fields']
    #     tasks['task_id'] = task['pk']
    #     from django.utils import dateparse
    #
    #     # tasks['exec_device'] = ServerInfo.objects.get(tasks['exec_device'])['server_name']
    #     #print(json.loads(serializers.serialize("json",ServerInfo.objects.get(server_id=tasks['exec_device']))))
    #     tasks['c_time'] = dateparse.parse_datetime(task['fields']['c_time'])
    #     datalist.append(task['fields'])
    #
    # print(datalist)
    # print(type(datalist))
    data_list = TaskList.objects.all()
    return render(request, 'performance/tasklist.html', locals())


def testjquery(request):
    return render(request, 'performance/testjquery.html')


def indextest(request, task_id=0):
    if task_id == 0:
        # 等于0说明是新进页
        taskid = 0
        busi_line = BusiLine.objects.all()
        return render(request, 'performance/index.html', locals())
    # 不等于 说明是编辑页 需要带信息过去，尤其是业务线和压测机的默认选择
    data = TaskList.objects.get(task_id=task_id)
    taskid = task_id
    busi_line = BusiLine.objects.all()
    print(data, taskid)
    return render(request, 'performance/index.html', locals())


def deltask(request):
    if request.method == 'GET':
        # print(request.GET.get("task_id"))
        try:
            TaskList.objects.get(task_id=request.GET.get("task_id")).delete()
        except Exception as e:

            return JsonResponse({'returncode': 500, 'errorMessage': e})
        data = {
            'returncode': 200, 'message': '删除成功'
        }
        return HttpResponse(json.dumps(data))


def getavalibleserver(request):
    if request.method == 'GET':
        # 数据库中获取状态为0的即可用的服务器
        server_list_queryset = ServerInfo.objects.filter(server_status=0).values_list('server_name')
        if len(server_list_queryset) >= 0:
            try:
                server_list = json.loads(serializers.serialize("json", ServerInfo.objects.filter(server_status=0),
                                                               fields=('server_name',)))
                server_avalible = [server['fields']['server_name'] for server in server_list]
                return JsonResponse({'returncode': 200, 'server_list': server_avalible})

            except Exception as e:
                # 无数据或者异常都抛出默认数据
                data = {
                    'returncode': 200,
                    'server_list': ['huawei', 'tencent']
                }
                return HttpResponse(json.dumps(data))
        return JsonResponse({'returncode': 200, 'server_list': ['huawei', 'tencent']})


@csrf_exempt
def saveplan(request):
    if request.method == "POST":
        task_name = request.POST.get("planName")
        busi_line = BusiLine.objects.get(busi_id=request.POST.get("busi"))
        test_url = request.POST.get("testUrl")
        threadCount = request.POST.get("threadCount")
        stepTime = request.POST.get("startTime")
        urlPrama = request.POST.get("urlParam")
        testTime = request.POST.get("testTime")
        exec_device = ServerInfo.objects.get(server_name=request.POST.get("state"))
        task_name_in = json.loads(
            serializers.serialize("json", TaskList.objects.filter(task_name=task_name), fields=('task_name',)))
        print(task_name_in)
        if len(task_name_in) != 0:
            # 判断是否已存在
            if task_name == task_name_in[0]['fields']['task_name']:
                # 判断是否已存在
                # 如果没有变化提示 return JsonResponse({"returncode": 200, "message": '，案例名称已存在，请勿重复提交'})

                return JsonResponse({"returncode": 20100, "message": '压测任务更新成功'})

            else:
                return JsonResponse({"returncode": 200, "message": '压测任务保存成功'})
        else:
            try:
                init = TaskList.objects.create(task_name=task_name, busi_line=busi_line, exec_device=exec_device,
                                               test_url=test_url, threadCount=threadCount, stepTime=stepTime,
                                               urlPrama=urlPrama,
                                               testTime=testTime)
                init.save()
            except Exception as e:
                return JsonResponse({"returncode": 200, "message": '保存失败', "info": e})
        return JsonResponse({"returncode": 200, "message": '压测任务保存成功'})



def execTask(request):
    pass