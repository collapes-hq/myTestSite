from django.conf.urls import url
from django.contrib import admin
from apitest import views
from django.urls import include, path


app_name = 'apitest'
urlpatterns = [
    url('manage/', view=views.apimanage),
    url('test/', view=views.test),
    url('editapi/$', view=views.editapi),
    url('saveapi/$', view=views.saveapi),
    url('apicase/', view=views.apicase),
    url('singlerequest/', view=views.singlerequest),
    url(r'caseadd/$', view=views.addapicase),
    url(r'addcase/$', view=views.addcase),
    url(r'editapi/(?P<api_id>[\d]{0,4})/$', view=views.editapi, name='jumpApi'),
    url(r'addcase/(?P<api_id>[\d]{0,4})/$', view=views.addcase, name='addcase'),
]
