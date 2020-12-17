# coding=utf-8

"""
@Author : haoqiang
@File   : tasks.py
@Time   : 2020/12/14 15:51
@Desc   : None

"""

from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def add():
    return 5


@shared_task
def mul(x, y):
    return x * y
