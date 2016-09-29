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
    url(r'^notificaIndex/$', views.notificaIndex, name='notifica'),
    url(r'^notificaIndexParticipation/$', views.notificaIndexParticipation, name='notificaParticipation'),
    url(r'^notificaIndexPosts/$', views.notificaIndexPosts, name='notificaPosts'),


    #Páginas de fix
    url(r'^create_fix/$', views.create_fix, name='create_fix'),
    url(r'^fix/(?P<pk>[0-9]+)/$', views.fix_detail, name='fix_detail'),
    url(r'^myfixies/$', views.my_fixies, name='myfixies'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>\w+)/participations/$', views.participations, name='participations'),
    url(r'^profile/(?P<username>\w+)/favorites/$', views.favorites, name='favorites'),
    url(r'^profile/(?P<username>\w+)/following/$', views.following, name='following'),
    url(r'^profile/(?P<username>\w+)/followers/$', views.follower, name='follower'),
    url(r'^participations/$', views.participationsSemUser, name='participations'),

    #Páginas de post
    url(r'^create_post/$', views.create_post, name='create_post'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^myposts/$', views.my_posts, name='my_posts'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.edit_post, name='edit_post'),

    #Rotas de requisiçoes AJAX - Fixies
        #My fixies
    url(r'^fix/(?P<pk>[0-9]+)/getnotifymyfix/$', views.getnotifymyfix, name='getnotifymyfix'),
    url(r'^fix/(?P<pk>[0-9]+)/inativenotifyfix/$', views.inativeNotifyMyFixies, name='inativeNotifyMyFixies'),
    url(r'^fix/(?P<pk>[0-9]+)/ativenotifyfix/$', views.ativeNotifyMyFixies, name='ativeNotifyMyFixies'),
    url(r'^fix/(?P<pk>[0-9]+)/delete_confirm/$', views.confirm_delete_fix, name='confirm_delete_fix'),
    url(r'^fix/(?P<pk>[0-9]+)/fixed/$', views.mark_fixed_code, name='mark_fixed_code'),
    url(r'^fix/(?P<pk>[0-9]+)/restore/$', views.to_restore_fixed_code, name='restore_fixed_code'),
    url(r'^fix/(?P<pk>[0-9]+)/best_answer/$', views.best_answer, name='best_answer'),
    url(r'^fix/(?P<pk>[0-9]+)/report/$', views.report_coment, name='report_coment'),

        #My participations
    url(r'^fix/(?P<pk>[0-9]+)/getnotifyparticipation/$', views.getnotifyparticipation, name='getnotifyparticipation'),
    url(r'^fix/(?P<pk>[0-9]+)/inativenotifyparticipate/$', views.inativeNotifyParticipations, name='inativeNotifyParticipations'),
    url(r'^fix/(?P<pk>[0-9]+)/ativenotifyparticipate/$', views.ativeNotifyParticipations, name='ativeNotifyParticipations'),
    url(r'^fix/(?P<pk>[0-9]+)/deleteparticipation/$', views.deleteParticipation, name='deleteParticipation'),

        #Visitante
    url(r'^fix/(?P<pk>[0-9]+)/getRelationshipFavorite/$', views.getRelationshipFavorite, name='getRelationshipFavorite'),
    url(r'^fix/(?P<pk>[0-9]+)/favorite/$', views.favorite_fix, name='favorite_fix'),
    url(r'^fix/(?P<pk>[0-9]+)/un_favorite/$', views.un_favorite_fix, name='un_favorite_fix'),

    #Rotas de requisições AJAX - Posts
    url(r'^post/(?P<pk>[0-9]+)/getkeypostprofile/$', views.getkeypostprofile, name='getkeypostprofile'),
    url(r'^post/(?P<pk>[0-9]+)/ativepostprofile/$', views.ativepostprofile, name='getkeypostprofile'),
    url(r'^post/(?P<pk>[0-9]+)/inativepostprofile/$', views.inativepostprofile, name='getkeypostprofile'),
    url(r'^post/(?P<pk>[0-9]+)/delete_post/$', views.delete_post, name='delete_post'),
    url(r'^post/(?P<pk>[0-9]+)/getkeyactivepost/$', views.getkeyactivepost, name='getkeyactivepost'),
    url(r'^post/(?P<pk>[0-9]+)/activenotifypost/$', views.ativeNotifyPost, name='activenotifypost'),
    url(r'^post/(?P<pk>[0-9]+)/inactivenotifypost/$', views.inativeNotifyPost, name='inactivenotifypost'),
    url(r'^post/(?P<pk>[0-9]+)/report/$', views.report_coment_post, name='report'),

        #Profile
    url(r'^profile/(?P<username>\w+)/getrelationship/$', views.getrelationship, name='getrelationship'),
    url(r'^profile/(?P<username>\w+)/follower/$', views.followajax, name='followajax'),
    url(r'^profile/(?P<username>\w+)/unfollower/$', views.unfollowajax, name='unfollowajax'),

]
