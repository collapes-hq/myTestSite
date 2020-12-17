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
CELERY_TIMEZONE = 'Asia/Shanghai'

# Broker配置，使用Redis作为消息中间件
# BROKER_URL = 'redis://:密码@主机地址:端口号/数据库号'
BROKER_URL = 'redis://:hq1234567@121.36.69.137:16397/1'

# BACKEND配置，这里使用redis
CELERY_RESULT_BACKEND = 'redis://:hq1234567@121.36.69.137:16397/2'

# celery到redis取任务每次取的个数
CELERYD_PREFETCH_MULTIPLIER = 4

# celery任务执行结果的超时时间
CELERY_TASK_RESULT_EXPIRES = 1200



CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 1200  # celery任务执行结果的超时时间

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
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYBEAT_SCHEDULE = {
    "course-task": {
        "task": "course-task",
        "schedule": crontab(hour=22, minute=50),
        "options": {
            "queue": "beat_queue"
        }
    }
}