# coding=utf-8

"""
@Author : haoqiang
@File   : celery.py
@Time   : 2020/12/14 14:50
@Desc   : None

"""

from __future__ import absolute_import
import os
from celery import Celery

# 设置django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytest.settings')
app = Celery('mytest')
#  使用CELERY_ 作为前缀，在settings中写配置
app.config_from_object('mytest.celery_config')
# 发现任务文件每个app下的task.py
app.autodiscover_tasks()
