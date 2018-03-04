"""storyhelper URL Configuration

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
from django.views.generic import RedirectView

from recorder import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/groups', permanent=True)),
    url(r'^groups/$', views.emloyee_groups),
    url(r'^groups/(?P<group_id>[0-9]+)/$', views.employees, name='home'),
    url(r'^groups/(?P<group_id>[0-9]+)/chart/$', views.group_chart),
    url(r'^employees/(?P<employee_id>[0-9]+)/$', views.machines),
    url(r'^employees/(?P<employee_id>[0-9]+)/(?P<machine_id>[0-9]+)/$', views.timestamp),
    url(r'^api/groups/(?P<group_id>[0-9]+)/$', views.group_chart_data),
    url(r'^admin/', admin.site.urls),
]
