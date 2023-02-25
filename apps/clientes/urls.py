# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.clientes import views

urlpatterns = [

    path('clientes', views.index, name='clientes'),
    path('clientes/cadastro', views.cadastro, name='clientes_cadastro'),
    path('clientes/atualiza/<int:id>', views.atualiza, name='clientes_atualiza'),
    path('clientes/deleta/<int:id>', views.deleta, name='clientes_deleta'),
    path('clientes/<int:id>/', views.detail, name='clientes_details'),

]
