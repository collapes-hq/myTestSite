# Generated by Django 3.1.3 on 2020-11-25 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0005_apicase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apicase',
            old_name='api_id',
            new_name='case_api_id',
        ),
    ]