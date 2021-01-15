# coding=utf-8

"""
@Author : haoqiang
@File   : celery_config.py
@Time   : 2020/12/14 15:04
@Desc   : None

"""

import djcelery
from celery.schedules import crontab

djcelery.setup_loader()  #

# 设置时区
# CELERY_TIMEZONE = 'Asia/Shanghai'
TIME_ZONE = 'Asia/Shanghai'
 
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
# Broker配置，使用Redis作为消息中间件
# BROKER_URL = 'redis://:密码@主机地址:端口号/数据库号'
BROKER_URL = 'redis://:hq1234567@121.36.69.137:16397/6'

# BACKEND配置，这里使用redis
# CELERY_RESULT_BACKEND = 'redis://:hq1234567@121.36.69.137:16397/5'
CELERY_RESULT_BACKEND = 'django-db'
# celery到redis取任务每次取的个数
CELERYD_PREFETCH_MULTIPLIER = 4

# celery任务执行结果的超时时间
# CELERY_TASK_RESULT_EXPIRES = 1200


CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 1200  # celery任务执行结果的超时时间
CELERY_TASK_ALWAYS_EAGER = True

# 设置任务队列
CELERY_QUEUES = {
    "beat_queue": {
        "exchange": "beat_queue",
        "exchange_type": "direct",
        "binding_key": "beat_queue"
    },
    "work_queue": {
        "exchange": "work_queue",
        "exchange_type": "direct",
        "binding_key": "work_queue"
    }
}

# 设置默认队列
CELERY_DEFAULT_QUEUE = "work_queue"


# 设置定时任务

from apitest import tasks
from datetime import timedelta
#from celery.schedules import crontab

CELERY_IMPORTS = ("apitest.tasks",)
CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERYBEAT_SCHEDULE = {
    "five-seconds-task": {
        "task": "apitest.tasks.addaaa",
        "schedule": timedelta(seconds=5),
	'args':(1,1)
	},
    "ten-seconds-task":{
	"task":"apitest.tasks.add",
	"schedule": timedelta(seconds=10),
	}
}
	

