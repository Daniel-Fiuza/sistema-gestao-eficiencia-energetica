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
    
    path('clientes/<int:cliente>/uc', views.clientes_uc, name='clientes_uc'),
    path('clientes/<int:cliente>/uc/cadastro', views.clientes_uc_cadastro, name='clientes_uc_cadastro'),
    path('clientes/<int:cliente>/uc/atualiza/<int:id>', views.clientes_uc_atualiza, name='clientes_uc_atualiza'),
    path('clientes/<int:cliente>/uc/deleta/<int:id>', views.clientes_uc_deleta, name='clientes_uc_deleta'),

    path('uc/<int:uc>/faturas', views.uc_faturas, name='uc_faturas'),
    path('uc/<int:uc>/faturas/cadastro', views.uc_faturas_cadastro, name='uc_faturas_cadastro'),
    path('uc/<int:uc>/faturas/atualiza/<int:id>', views.uc_faturas_atualiza, name='uc_faturas_atualiza'),
    path('uc/<int:uc>/faturas/deleta/<int:id>', views.uc_faturas_deleta, name='uc_faturas_deleta'),
    
]   
