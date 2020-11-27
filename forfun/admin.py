from django.contrib import admin
from forfun import models
# Register your models here.
admin.site.register(models.Keyword)
admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Article)