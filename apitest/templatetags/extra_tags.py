# coding=utf-8

"""
@Author : haoqiang
@File   : extra_tags.py.py
@Time   : 2020/12/8 10:28
@Desc   : None

"""

from django import template
from apitest import models

register = template.Library()


@register.filter()
def strToList(value):
    # eval(value.replace("true", "\'true\'").repalce("false", "\'false\'"))
    result = str(value.replace("true", "\'true\'")).replace("false", "\'false\'")
    return eval(result)


@register.filter()
def strToDict(value):
    cases = eval(value.replace("true", "\'true\'").replace("false", "\'false\'"))
    case_list = []
    for case in cases:
        case_list.append(case["importUnitName"])
    return case_list


@register.filter()
def getCaseCount(value):
    count = len(models.apiCase.objects.filter(case_api_id=value))
    return count


@register.filter()
def getSuccessSum(value):
    data = models.taskResultDetail.objects.filter(task_id=value)
    count = 0
    for item in data:
        count += len(eval(item.taskResult_success))
    return count


@register.filter()
def getFailureSum(value):
    data = models.taskResultDetail.objects.filter(task_id=value)
    count = 0
    for item in data:
        count += len(eval(item.taskResult_failure))
    return count
