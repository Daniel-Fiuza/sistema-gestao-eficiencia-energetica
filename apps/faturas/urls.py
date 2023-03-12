# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.faturas import views

urlpatterns = [

    path('faturas', views.faturas, name='faturas'),
    path('faturas/<int:id>/download', views.download, name='faturas_download'),

]
