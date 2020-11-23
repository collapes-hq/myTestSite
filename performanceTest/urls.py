# coding=utf-8

"""
@Author : haoqiang
@File   : urls.py.py
@Time   : 2020/11/3 15:30
@Desc   : None

"""

from django.conf.urls import url
from django.contrib import admin
from performanceTest import views

app_name = 'performanceTest'

urlpatterns = [
    url(r'tasklist/', view=views.tasklist, ),
    url(r'testjquery/', view=views.testjquery),
    url(r'^dashboard/$', view=views.firstpage),
    url(r'performanceTest/indextest/$', view=views.indextest),
    url(r'performanceTest/getServerCount/$', view=views.getServerCount),
    url(r'performanceTest/savePlan/$', view=views.saveplan),
    url(r'performanceTest/deltask/$', view=views.deltask),
    url(r'performanceTest/taskresultlist/$', view=views.taskresult),
    url(r'performanceTest/getavailbleserver/', view=views.getavalibleserver),
    # url(r'performanceTest/indextest/(?P<task_name>[\w-]+)/$', view=views.indextest, name='paramtest'),
    url(r'^performanceTest/indextest/(?P<task_id>[\d]{0,4})/$', view=views.indextest, name='paramtest'),
    url(r'^performanceTest/exectask/(?P<task_id>[\d]{0,4})/$', view=views.exectask, name='tasktest'),


]
