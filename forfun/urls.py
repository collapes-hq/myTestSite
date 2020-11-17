# coding=utf-8
"""
@Author : haoqiang
@File   : urls.py
@Time   : 2020/11/13 15:10
@Desc   : None

"""
from django.conf.urls import url
from forfun import views

urlpatterns = [
    url('^forfun/wordCloud/', view=views.wordCloud),
    url('^forfun/servermanage/', view=views.servermanage),
    url('^forfun/delserver/', view=views.delserver),
    url('^forfun/saveServerInfo/', view=views.saveServerInfo),
]
