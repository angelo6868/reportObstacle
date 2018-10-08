"""Reportobstacle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from web import views
from backend import views as backend_views

urlpatterns = [
    path('admin/', admin.site.urls),

    url('^(?P<username>\w+)/upload-avatar/$', backend_views.upload_avatar),
    url('^process-comment/$', views.process_comment),
    url('^backend/', include('backend.url')),
    url('^pictures/(\w+)/$', views.upload_pictures),
    url('^logoff/$', views.logoff),
    url('^up_down/$', views.up_down),
    url('^homepage/(?P<label_id>\d).html/$', views.homepage),
    url('homepage/$', views.homepage),
    url('register/$', views.register),
    url('login/$', views.login),
    url('test/$', views.test),
    url('identify_code/$', views.identify_code),
    url('(?P<username>[^/]+)/(?P<option>\w+)/(?P<id>[^/]+)\.html/$', views.personal_choose_page),
    url('(?P<username>[^/]*)/manage_edit-(?P<tag_id>\d+)-(?P<classification_id>\d+)/$', views.manage_edit),
    url('(?P<username>[^/]*)/manage_tag/$', backend_views.manage_tag),
    url('(?P<username>[^/]*)/manage_classification/$', backend_views.manage_classification),
    url('(?P<username>[^/]*)/manage_user_info/$', backend_views.manage_user_info),
    url('(?P<username>[^/]*)/manage_user_obstacle-(?P<status_id>\d+)/$', backend_views.manage_user_obstacle),

    url('(?P<username>\w+)/backend/add-article/$', backend_views.add_article),
    url('(?P<username>\w+)/add-obstacle/$', backend_views.add_obstacle),
    url('(?P<username>\w+)/backend/add-tag/$', backend_views.add_tag),
    url('(?P<username>\w+)/backend/add-classification/$', backend_views.add_classification),
    url('(?P<username>[^/]*)/(?P<id>[^/]*)\.html/$', views.article_page),
    url('[^/]+\.html/$', views.personal_page),
]
