# Generated by Django 3.1.2 on 2020-12-10 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0009_monitortask_monitortask_cron'),
    ]

    operations = [
        migrations.CreateModel(
            name='taskResultDetail',
            fields=[
                ('taskexec_id', models.AutoField(primary_key=True, serialize=False, verbose_name='任务结果编号')),
                ('task_id', models.IntegerField(blank=True, null=True, verbose_name='任务id')),
                ('taskResult_success', models.CharField(blank=True, max_length=1024, null=True, verbose_name='请求成功的记录')),
                ('taskResult_failure', models.CharField(blank=True, max_length=1024, null=True, verbose_name='请求失败的记录')),
                ('taskexec_startTime', models.DateTimeField(verbose_name='开始执行时间')),
                ('taskexec_endTime', models.DateTimeField(verbose_name='执行结束时间')),
            ],
        ),
        migrations.AddField(
            model_name='apicase',
            name='apicase_returncode',
            field=models.IntegerField(blank=True, null=True, verbose_name='期望returncode'),
        ),
    ]