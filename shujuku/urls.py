"""shujuku URL Configuration

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
from django_web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login),
    url(r'^register/$', views.register,name='register'),
    url(r'^index/$', views.index,name='index'),
    url(r'^xiugaipassword/$', views.xiugai,name='xiugai'),
    url(r'^table/$', views.table,name='table'),
    url(r'^show_asset_in_table/$', views.show_asset_in_table,name='show_asset_in_table'),
    url(r'^show_asset_in_table2/$', views.show_asset_in_table2,name='show_asset_in_table2'),
    url(r'^show_asset_in_table3/$', views.show_asset_in_table3,name='show_asset_in_table3'),
    url(r'^dingdan/$', views.dingdan,name='dingdan'),
    url(r'^zhifu/$', views.zhifu,name='zhifu'),
    url(r'^a/$', views.a,name='a'),
    url(r'^b/$', views.b,name='b'),
    url(r'^c/$', views.c,name='c'),
    url(r'^d/$', views.d,name='d'),
    url(r'^e/$', views.e,name='e'),
    url(r'^songshui/$', views.songshui,name='songshui'),
    url(r'^songshu/$', views.songshu,name='songshu'),
    url(r'^jiedan/$', views.jiedan, name='jiedan'),
    url(r'^jiedan2/$', views.jiedan2,name='jiedan2'),
    url(r'^employerregister/$', views.employerregister,name='employerregister'),
]
