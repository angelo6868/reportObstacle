from django.conf.urls import url
from backend import views as backend_views
from web import views

urlpatterns = [
    url('create-blog/$', views.create_blog),
    url('edit-article-(?P<nid>\d+)\.html/$', views.edit_article),
    url('edit-obstacle-(?P<nid>\d+)\.html/$', backend_views.edit_obstacle),
    url('handel-obstacle-(?P<nid>\d+)\.html/$', backend_views.handel_obstacle),
    url('handel-solution-obstacle-(?P<nid>\d+)\.html/$', backend_views.handel_obstacle_solution),
    url('check-obstacle-(?P<nid>\d+)\.html/$', backend_views.check_obstacle),
    url('delete-obstacle-(?P<nid>\d+)\.html/$', backend_views.delete_obstacle),
    url('edit-tag-(?P<nid>\d+)\.html/$', backend_views.edit_tag),
    url('edit-classification-(?P<nid>\d+)\.html/$', backend_views.edit_classification),
    url('delete-tag-(?P<nid>\d+)\.html/$', backend_views.delete_tag),
    url('handel_user_obstacle-(\d+)/$', backend_views.handel_obstacle_list),
    url('handel-obstacle-add-(?P<nid>\d+)/$', backend_views.handel_obstacle_add),
    url('delete-classification-(?P<nid>\d+)\.html/$', backend_views.delete_classification),
]