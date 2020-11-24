# Generated by Django 3.1.3 on 2020-11-18 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiinfo',
            name='api_type',
            field=models.IntegerField(blank=True, choices=[(0, 'get'), (1, 'post')], max_length=64, null=True, verbose_name='请求类型'),
        ),
    ]