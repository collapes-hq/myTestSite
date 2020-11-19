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
        ordering = ['-api_c_time'],
