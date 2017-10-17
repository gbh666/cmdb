#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sam"
# Date: 2017/10/11


from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^server.html$', views.server),
    url(r'^server_json.html$', views.server_json),
    url(r'^disk.html$', views.disk),
    url(r'^disk_json.html$', views.disk_json),
    url(r'^memory.html$', views.memory),
    url(r'^memory_json.html$', views.memory_json),
    url(r'^nic.html$', views.nic),
    url(r'^nic_json.html$', views.nic_json),
    url(r'^test.html$', views.test),
]