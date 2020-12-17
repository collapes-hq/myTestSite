from django.db import models


# Create your models here.

class apiInfo(models.Model):
    type = (
        (0, 'get'),
        (1, 'post'),
    )
    contenttype = (
        (1, 'NONE'),
        (2, 'URL-ENCODE'),
        (3, 'JSON'),
    )
    api_id = models.AutoField(primary_key=True, verbose_name='接口序号')
    api_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='接口名称')
    api_busi = models.ForeignKey('performanceTest.BusiLine', null=True, verbose_name='业务线', on_delete=models.SET_NULL)
    api_type = models.IntegerField(choices=type, null=True, blank=True, verbose_name='请求类型')
    api_url = models.URLField(max_length=256, null=True, blank=True, verbose_name='请求地址')
    api_contenttype = models.IntegerField(choices=contenttype, null=True, blank=True, verbose_name='参数类型')
    api_headers = models.CharField(max_length=256, null=True, blank=True, verbose_name='请求头参数')
    api_content = models.CharField(max_length=256, null=True, blank=True, verbose_name='请求正文')
    api_apidesc = models.CharField(max_length=256, null=True, blank=True, verbose_name='接口描述')
    api_c_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Mate:
        verbose_name = '接口信息表',
        verbose_name_plural = '接口信息表',
        ordering = ['api_c_time'],


class apiCase(models.Model):
    apicase_id = models.AutoField(primary_key=True, verbose_name='case编号')
    apicase_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='用例名称')
    apicase_desc = models.CharField(max_length=256, null=True, blank=True, verbose_name='用例描述')
    case_api = models.ForeignKey('apiInfo', null=True, blank=True,default=0,on_delete= models.SET_NULL)
    case_busi = models.ForeignKey('performanceTest.BusiLine', null=True, blank=True, on_delete=models.SET_NULL)
    apicase_params = models.CharField(max_length=256, null=True, blank=True, verbose_name='请求参数')
    apicase_returncode = models.IntegerField(null=True, blank=True, verbose_name='期望returncode')
    apicase_express = models.CharField(max_length=256, null=True, blank=True, verbose_name='表达式')
    apicase_except = models.CharField(max_length=256, null=True, blank=True, verbose_name='期望值')
    apicase_c_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Mate:
        verbose_name = '接口用例表',
        verbose_name_plural = '接口用例表',
        ordering = ['apicase_c_time'],


class monitorTask(models.Model):
    type = (
        (0, '自动'),
        (1, '手动'),
    )
    monitorTask_id = models.AutoField(primary_key=True, verbose_name='任务编号')
    monitorTask_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='任务名称')
    monitorTask_type = models.IntegerField(choices=type, null=True, blank=True, verbose_name='任务类型')
    monitorTask_caseList = models.CharField(max_length=256, null=True, blank=True, verbose_name='用例列表')
    monitorTask_busi = models.ForeignKey('performanceTest.BusiLine', null=True, verbose_name='业务线',
                                         on_delete=models.SET_NULL)
    monitorTask_c_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    monitorTask_cron = models.CharField(max_length=64, null=True, blank=True, verbose_name='执行cron')

    class Mate:
        verbose_name = '巡查任务用例表',
        verbose_name_plural = '巡查任务用例表',
        ordering = ['monitorTask_c_time'],


class taskResultDetail(models.Model):
    taskexec_id = models.AutoField(primary_key=True, verbose_name='任务结果编号')
    task_id = models.IntegerField(null=True, blank=True, verbose_name='任务id')
    taskResult_success = models.CharField(max_length=1024, null=True, blank=True, verbose_name='请求成功的记录')
    taskResult_failure = models.CharField(max_length=1024, null=True, blank=True, verbose_name='请求失败的记录')
    taskexec_startTime = models.DateTimeField(verbose_name='开始执行时间')
    taskexec_endTime = models.DateTimeField(verbose_name='执行结束时间')

    class Mate:
        verbose_name = '巡查任务结果detail表',
        verbose_name_plural = '巡查任务结果detail表',
        ordering = ['taskexec_startTime'],
