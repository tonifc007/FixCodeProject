# -*- coding: utf 8 -*-
from django.conf.urls import url
from . import views

app_name = 'core'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^editprofile/$', views.edit_details_profile, name='editprofile'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^create_fix/$', views.create_fix, name='create_fix'),
    url(r'^fix/(?P<pk>[0-9]+)/delete/$', views.delete_fix, name='delete_fix'),
    url(r'^fix/(?P<pk>[0-9]+)/delete_confirm/$', views.confirm_delete_fix, name='confirm_delete_fix'),
    url(r'^fix/(?P<pk>[0-9]+)/$', views.fix_detail, name='fix_detail'),
    url(r'^fix/(?P<fixpk>[0-9]+)/best_answer/(?P<compk>[0-9]+)/$', views.best_answer, name='best_answer'),
    url(r'^fix/(?P<pk>[0-9]+)/fixed/$', views.mark_fixed_code, name='mark_fixed_code'),
    url(r'^fix/(?P<pk>[0-9]+)/restore/$', views.to_restore_fixed_code, name='restore_fixed_code'),
    url(r'^myfixies/$', views.my_fixies, name='myfixies'),
    url(r'^profile/(?P<username>\w+)/participations/$', views.participations, name='participations'),
    url(r'^fix/(?P<pk>[0-9]+)/favorite/$', views.favorite_fix, name='favorite_fix'),
    url(r'^fix/(?P<pk>[0-9]+)/un_favorite/$', views.un_favorite_fix, name='un_favorite_fix'),
    url(r'^profile/(?P<username>\w+)/favorites/$', views.favorites, name='favorites'),
    url(r'^profile/(?P<username>\w+)/follow/$', views.follow, name='follow'),
    url(r'^profile/(?P<username>\w+)/unfollow/$', views.unfollow, name='unfollow'),
    url(r'^profile/(?P<username>\w+)/following/$', views.following, name='following'),
    url(r'^profile/(?P<username>\w+)/followers/$', views.follower, name='follower'),
]
