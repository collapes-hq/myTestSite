from django.shortcuts import render
from performanceTest.models import ServerInfo
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect


# Create your views here.
def wordCloud(request):
    return render(request, 'wordCloud.html', locals())


def servermanage(request):
    serverlist = ServerInfo.objects.all()
    serverstatus = [
        {'statacode': 0, 'statavalue': '可用'},
        {'statacode': 1, 'statavalue': '忙碌'},
        {'statacode': 2, 'statavalue': '下线'},
    ]
    return render(request, 'servermanage.html', locals())


def delserver(request):
    if request.method == 'GET':
        server_name = request.GET.get('servername')
        # 这个传过来的servername是 tencent_123\n,坑人

        try:
            a = ServerInfo.objects.filter(server_name=server_name.strip())
            a.delete()
        except Exception as e:
            return JsonResponse({'returncode': 500, 'message': e})
        return JsonResponse({'returncode': 200, 'message': '删除成功'})


@csrf_exempt
def saveServerInfo(request):
    if request.method == "POST":
        server_name = request.POST.get("server_name")
        server_ip = request.POST.get("server_ip")
        server_cloud = request.POST.get("server_cloud")
        server_status = request.POST.get("server_status")
        servers = ServerInfo.objects.filter(server_name=server_name)
        if not servers:
            init = ServerInfo.objects.create(server_name=server_name, server_ip=server_ip, server_cloud=server_cloud,
                                             server_status=server_status)
            print(1)
            init.save()
        else:
            for server in servers:
                server.server_ip = server_ip
                server.server_cloud = server_cloud
                server.server_status = server_status
                print(2)
                server.save()
        # print(server_name, server_ip, server_cloud, server_status)
        return JsonResponse({'returncode': 200, 'message': '保存成功'})
