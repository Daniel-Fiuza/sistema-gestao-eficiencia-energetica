# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import mimetypes
import os
from urllib.parse import unquote
from django.conf import settings
from django.http import FileResponse
from apps.home.indicadores import Indicadores, TIME_FILTER
from apps.clientes.models import UC


@login_required(login_url="/login/")
def index(request):
    # Parâmetros de Filtro
    uc_filter = request.GET.get('uc_filter', None)
    uc_filter = uc_filter.split(' - ')[0] if uc_filter is not None else None
    time_filter = request.GET.get('time_filter', None)

    # UC Opções de Entrada
    uc_options = UC.objects.all()
    time_options = list(TIME_FILTER.keys())

    # Cálculo dos Indicadores
    uc_input = uc_filter if uc_filter is not None else uc_options.first().numero_uc
    time_input = time_filter if time_filter is not None else time_options[0]
    
    indicadores = Indicadores(uc_input, time_input)
    indicadores.efetua_calculos()

    # Definição do contexto
    context = {
        'segment': 'index',
        'uc_options': uc_options,
        'uc_selected': uc_input, 
        'time_options': time_options, 
        'time_selected': time_input,
        'indicadores': indicadores
    }

    html_template = loader.get_template('home/index.html')  
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        media = True if request.path.split('/')[1] == 'media' else False

        if media:
            mimetype, _ = mimetypes.guess_type(request.path, strict=True)
            if not mimetype:
                mimetype = "text/html"

            path = '/'.join(request.path.split('/')[2:])
            filepath = os.path.join(settings.MEDIA_ROOT, path)
            filepath = unquote(os.path.join(settings.MEDIA_ROOT, path)).encode("utf-8")
            return FileResponse(open(filepath, "rb"), content_type=mimetype)
    
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
        