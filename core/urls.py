# -*- coding: utf 8 -*-
from django.conf.urls import url
from . import views

app_name = 'core'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^create_fix/$', views.create_fix, name='create_fix'),
    url(r'^fix/(?P<pk>[0-9]+)/$', views.fix_detail, name='fix_detail'),
    url(r'^fix/(?P<fixpk>[0-9]+)/best_answer/(?P<compk>[0-9]+)/$', views.best_answer, name='best_answer'),
    url(r'^fix/(?P<pk>[0-9]+)/fixed/$', views.mark_fixed_code, name='mark_fixed_code'),
    url(r'^fix/(?P<pk>[0-9]+)/restore/$', views.to_restore_fixed_code, name='restore_fixed_code')
]
