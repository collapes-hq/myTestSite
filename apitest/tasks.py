# coding=utf-8

"""
@Author : haoqiang
@File   : tasks.py
@Time   : 2020/12/14 15:51
@Desc   : None

"""

from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time


@shared_task
def addaaa(a, b):
    time.sleep(5)
    sum = a + b
    return sum

@shared_task
def add():
   time.sleep(2)
   return 6
