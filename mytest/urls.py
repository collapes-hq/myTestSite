"""mytest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from usermanage import views
from django.urls import include, path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('forfun.urls')),
    url(r'^api/', include('apitest.urls')),
    # url(r'^dashboard$', include('performanceTest.urls')),
    url(r'^test/', view=views.test),
    url(r'^login/', view=views.login),
    url(r'^register/', view=views.register),
    url(r'^logout/', view=views.logout),
    url(r'^getCpuLoad/', view=views.getCpuLoad),
    url(r'^scripttest/', view=views.scripttest),
    url(r'^uploadfile/', view=views.saveFile),
    # url(r'^captcha', include('captcha.urls')),
    # url(r'^test/', include('performanceTest.urls')),
    path('', include('performanceTest.urls'))

]
