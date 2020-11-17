from django.contrib import admin

# Register your models here.
from performanceTest import models

admin.site.register(models.ServerInfo)
admin.site.register(models.TaskList)
admin.site.register(models.BusiLine)