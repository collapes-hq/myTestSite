from django.conf.urls import url
from django.contrib import admin
from apitest import views
from django.urls import include, path


urlpatterns = [
    url('manage/',view=views.apimanage),
    url('editapi/',view=views.editapi),
    url('saveapi/',view=views.saveapi),
]