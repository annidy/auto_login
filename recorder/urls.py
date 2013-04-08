# -*- coding:utf8 -*-
from django.conf.urls import patterns, include, url
from recorder import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^welcome/', views.welcome),
    url(r'^start/', views.start),
    url(r'^stop/', views.stop),
    url(r'^query/',views.api_query), # 查询 /query?un=???
)