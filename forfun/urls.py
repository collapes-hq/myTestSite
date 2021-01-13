# coding=utf-8
"""
@Author : haoqiang
@File   : urls.py
@Time   : 2020/11/13 15:10
@Desc   : None

"""
from django.conf.urls import url
from forfun import views
from django.urls import path

app_name = 'forfun'
urlpatterns = [
    url('^forfun/wordCloud/', view=views.wordCloud),
    url('^forfun/blog/', view=views.blogpage),
    url('^forfun/cityChoice/', view=views.citychoice),
    url('^forfun/servermanage/', view=views.servermanage),
    url('^forfun/delserver/', view=views.delserver),
    url('^forfun/saveServerInfo/', view=views.saveServerInfo),
    # url(r'^article/(?P<slug>[\w-]+)/$', view=views.detail, name='detail'),  # 文章内容页
    path(r'article/<slug:slug>/', view=views.detail, name='detail'),  # 文章内容页
    path(r'category/<slug>/', view=views.category, name='category'),
    url(r'^tag/(?P<slug>[\w-]+)/$', view=views.detail, name='tag'),
]
