from django.db import models


# Create your models here.


class TaskList(models.Model):
    task_id = models.AutoField(primary_key=True, verbose_name='序号')
    task_name = models.CharField(max_length=256, null=True, blank=True, unique=True, verbose_name='任务名称')
    busi_line = models.ForeignKey('BusiLine', null=True, verbose_name='业务线', on_delete=models.SET_NULL)
    exec_device = models.ForeignKey('ServerInfo', null=True, verbose_name='所选压测机', on_delete=models.SET_NULL)
    test_url = models.URLField(max_length=256)
    threadCount = models.IntegerField(null=True, blank=True)
    stepTime = models.IntegerField(null=True, blank=True)
    urlPrama = models.CharField(max_length=256, null=True, blank=True)
    testTime = models.IntegerField(null=True, blank=True)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    s_time = models.DateTimeField(auto_now=True, verbose_name='变更时间')

    class Mate:
        verbose_name = '任务表',
        verbose_name_plural = '任务表',
        ordering = ['-s_time'],


class BusiLine(models.Model):
    busi_id = models.IntegerField()
    busi_name = models.CharField(max_length=128, blank=True)


class ServerInfo(models.Model):
    cloud = (
        ('huaweiCloud', '华为云'),
        ('tencentCloud', '腾讯云'),
        ('aliCloud', '阿里云'),
    )
    status = (
        (0, '可用'),
        (1, '忙碌'),
        (2, '下线'),
    )
    server_id = models.AutoField(primary_key=True, verbose_name='压测机编号')
    server_name = models.CharField(max_length=64, verbose_name='压测机名称', unique=True)
    server_cloud = models.CharField(choices=cloud, max_length=64, verbose_name='所属服务商')
    server_ip = models.GenericIPAddressField('IP地址', null=True, blank=True)
    server_status = models.IntegerField(choices=status)
    add_time = models.DateTimeField(auto_now_add=True)

    class Mate:
        verbose_name = '压测机信息表'
        verbose_name_plural = '压测机信息表'
        ordering = ['-add_time']


class TaskResult(models.Model):
    task_id = models.IntegerField()
    task_name = models.CharField(max_length=256, null=True, blank=True)
    exec_device = models.ForeignKey(ServerInfo, null=True, verbose_name='所选压测机', on_delete=models.SET_NULL)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    s_time = models.DateTimeField(auto_now=True, verbose_name='变更时间')
