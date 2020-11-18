from django.shortcuts import render
from django.http import JsonResponse
from apitest.models import apiInfo
from performanceTest.models import BusiLine
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def apimanage(request):
    apilist = apiInfo.objects.all()

    return render(request, 'apimanage.html', locals())


def editapi(request):
    apilist = apiInfo.objects.all()
    busi_line = BusiLine.objects.all()
    return render(request, 'editapi.html', locals())


@csrf_exempt
def saveapi(request):
    print(1)
    if request.method == "POST":
        apiname = request.POST.get("apiname")
        header_key = request.POST.getlist("headerkey")
        header_value = request.POST.getlist("headervalue")
        apiurl = request.POST.get("apiurl")
        apidesc = request.POST.get("apidesc")
        method = request.POST.get("method")
        contenttype = request.POST.get("contenttype")
        apicontent = request.POST.get("apicontent")

        # param_zip = zip([a for a in key if a is not ""], [b for b in value if b is not ""])
        if apiInfo.objects.filter(api_name=apiname).exist():
            param_dict = {}
            for k, v in zip(header_key, header_value):
                if k not in [None, ""] and v not in [None, ""]:
                    param_dict[k] = v
            print(param_dict)
        else:
            return JsonResponse({"returncode": 200, "message": "接口名称已存在"})
        return JsonResponse({'returncode': 200})
