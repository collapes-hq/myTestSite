# Generated by Django 3.1.5 on 2021-01-14 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performanceTest', '0008_auto_20201124_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklist',
            name='task_name',
            field=models.CharField(blank=True, max_length=252, null=True, unique=True, verbose_name='任务名称'),
        ),
    ]
