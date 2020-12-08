# Generated by Django 3.1.2 on 2020-12-07 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performanceTest', '0008_auto_20201124_1746'),
        ('apitest', '0007_auto_20201207_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='monitorTask',
            fields=[
                ('monitorTask_id', models.AutoField(primary_key=True, serialize=False, verbose_name='任务编号')),
                ('monitorTask_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='任务名称')),
                ('monitorTask_type', models.IntegerField(blank=True, choices=[(0, '自动'), (1, '手动')], null=True, verbose_name='任务类型')),
                ('monitorTask_caseList', models.CharField(blank=True, max_length=256, null=True, verbose_name='用例列表')),
                ('monitorTask_c_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('monitorTask_busi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='performanceTest.busiline', verbose_name='业务线')),
            ],
        ),
    ]