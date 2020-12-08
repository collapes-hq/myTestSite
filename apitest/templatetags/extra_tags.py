# coding=utf-8

"""
@Author : haoqiang
@File   : extra_tags.py.py
@Time   : 2020/12/8 10:28
@Desc   : None

"""

from django import template

register = template.Library()

@register.filter()
def strToList(value):
    # eval(value.replace("true", "\'true\'").repalce("false", "\'false\'"))
    result = str(value.replace("true", "\'true\'")).replace("false", "\'false\'")
    return eval(result)
