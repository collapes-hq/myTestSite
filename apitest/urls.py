from django.conf.urls import url
from django.contrib import admin
from apitest import views
from django.urls import include, path


app_name = 'apitest'
urlpatterns = [
    url('manage/', view=views.apimanage),
    url('celerytest/', view=views.celerytest),
    # url('celerytestapi/', view=views.celerytestapi),
    url('editapi/$', view=views.editapi),
    url('saveapi/$', view=views.saveapi),
    url('taskedit/$', view=views.task_name_get_taskinfo),
    url('apicase/', view=views.apicase),
    url('singlerequest/', view=views.singlerequest),
    url(r'caseadd/$', view=views.addapicase),
    url(r'delcase/$', view=views.delcase),
    url(r'addcase/$', view=views.addcase),
    url(r'delapi/$', view=views.delapi),
    url(r'timingTask/$', view=views.timingTask),
    url(r'monitorTask/$', view=views.monitorTask),
    url(r'singleTaskInfo/(?P<task_id>[\d]{0,4})/$', view=views.singleTaskDetail,name='taskDetail'),
    url(r'getdata/$', view=views.getdata),
    url(r'patrolTaskcase/$', view=views.addMonitorCase),
    url(r'manualExecTask/$', view=views.manualExecTask),
    url(r'busicaselist/$', view=views.getcaselist),
    url(r'editapi/(?P<api_id>[\d]{0,4})/$', view=views.editapi, name='jumpApi'),
    url(r'addcase/(?P<api_id>[\d]{0,4})/$', view=views.addcase, name='addcase'),
    url(r'sendsinglecase/(?P<api_id>[\d]{0,4})/(?P<case_id>[\d]{0,4})/$', view=views.singlecase, name='singlecase'),
]
