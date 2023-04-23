from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Clientes, UC
from .forms import CadastroClienteForm, CadastroUCForm
from django.forms.models import model_to_dict
from apps.faturas.models import Faturas
from apps.faturas.forms import CadastroFaturaModelForm, DadosFaturaModelForm
from django.core.files.storage import FileSystemStorage
from apps.ETL import FaturaBaseDB
from apps.faturas.models import DadosFaturas
from django.conf import settings
import os

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    clientes = Clientes.objects.all()
    html_template = loader.get_template('clientes/index.html')
    return HttpResponse(html_template.render({'clientes':clientes}))


@login_required(login_url="/login/")
def detail(request, id):
    return HttpResponse('<h1>Implementado em breve.</h1>')


@login_required(login_url="/login/")
def cadastro(request):
    if request.method == 'POST':
        form = CadastroClienteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = CadastroClienteForm()
    return render(request, 'clientes/cadastro.html', {'form': form})


@login_required(login_url="/login/")
def atualiza(request, id):
    cliente = get_object_or_404(Clientes, id=id)
    form = CadastroClienteForm(instance=cliente)

    if request.method == 'POST':
        form = CadastroClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            return redirect('clientes')
        
    return render(request, 'clientes/atualiza.html', {'form': form})


@login_required(login_url="/login/")
def deleta(request, id):
    cliente = get_object_or_404(Clientes, id=id)
    cliente.delete()

    return redirect('clientes')


@login_required(login_url="/login/")
def clientes_uc(request, cliente):
    cliente_instance = get_object_or_404(Clientes, id=cliente)
    UCs = UC.objects.filter(cliente=cliente_instance)

    html_template = loader.get_template('uc/index.html')
    return HttpResponse(html_template.render({'UCs':UCs, 'cliente': cliente_instance}))


@login_required(login_url="/login/")
def clientes_uc_cadastro(request, cliente):
    print('cliente: ', cliente)
    client_instance = get_object_or_404(Clientes, id=cliente)
    print('cliente instance: ', client_instance)
    if request.method == 'POST':
        form = CadastroUCForm(request.POST)

        if form.is_valid():
            uc = form.save(commit=False)
            uc.cliente = client_instance
            uc.save()
            print(model_to_dict(uc))
            return redirect('clientes_uc', cliente=cliente)
    else:
        form = CadastroUCForm()
    return render(request, 'uc/cadastro.html', {'form': form, 'cliente_id': cliente})


@login_required(login_url="/login/")
def clientes_uc_atualiza(request, cliente, id):
    uc = get_object_or_404(UC, id=id)
    form = CadastroUCForm(instance=uc)

    if request.method == 'POST':
        form = CadastroUCForm(request.POST, instance=uc)

        if form.is_valid():
            form.save()
            return redirect('clientes_uc', cliente=cliente)
        
    return render(request, 'uc/atualiza.html', {'form': form, 'cliente_id': cliente})



@login_required(login_url="/login/")
def clientes_uc_deleta(request, cliente, id):
    uc = get_object_or_404(UC, id=id)
    uc.delete()
    return redirect('clientes_uc', cliente=cliente)


@login_required(login_url="/login/")
def uc_faturas(request, uc):
    uc = get_object_or_404(UC, id=uc)
    faturas = Faturas.objects.all()

    html_template = loader.get_template('faturas/index.html')
    return HttpResponse(html_template.render({'Faturas':faturas, 'UC': uc.id}))


@login_required(login_url="/login/")
def uc_faturas_cadastro(request, uc):
    uc_instance = get_object_or_404(UC, id=uc)
    
    if request.method == 'POST' and request.FILES['fatura']:
        form = CadastroFaturaModelForm(request.POST, request.FILES)

        if form.is_valid():
            fatura = form.save(commit=False)
            fatura.uc_id = uc_instance
            fatura.save()

            filename = os.path.join(settings.MEDIA_ROOT, fatura.fatura.name)

            try:
                etl_fatura = FaturaBaseDB(filename, DadosFaturas)
                dadosfatura_id = etl_fatura.extrair()
                
                dadosfatura = DadosFaturas.objects.get(id=dadosfatura_id)
                dadosfatura.fatura_id = fatura
                dadosfatura.uc_id = uc_instance
                dadosfatura.mes_ano_fatura = fatura.mes_ano
                dadosfatura.save()

            except:
                dados = {field: 0.0 for field in DadosFaturaModelForm().fields.keys()}
                dados['fatura_id'] = fatura
                dados['uc_id'] = uc_instance
                dados['mes_ano_fatura'] = fatura.mes_ano
                DadosFaturas.objects.create(**dados)           

            return redirect('uc_faturas', uc=uc)
    else:
        form = CadastroFaturaModelForm()
    return render(request, 'faturas/cadastro.html', {'form': form, 'uc': uc})


@login_required(login_url="/login/")
def uc_faturas_atualiza(request, uc, id):
    fatura = get_object_or_404(Faturas, id=id)
    form = CadastroFaturaModelForm(instance=fatura)

    if request.method == 'POST' and request.FILES['fatura']:
        form = CadastroFaturaModelForm(request.POST, request.FILES, instance=fatura)

        if form.is_valid():
            form.save()
            return redirect('uc_faturas', uc=uc)
        
    return render(request, 'faturas/atualiza.html', {'form': form, 'uc': uc})


@login_required(login_url="/login/")
def uc_faturas_dados(request, uc, id):
    fatura = get_object_or_404(Faturas, id=id)
    dados_fatura = fatura.dadosfaturas_set.all()
    form = DadosFaturaModelForm()
    dados_fatura_instance = None

    if dados_fatura:
        dados_fatura_instance = dados_fatura.first()
        form = DadosFaturaModelForm(instance=dados_fatura_instance)

    if request.method == 'POST':
        form = DadosFaturaModelForm(request.POST)

        if dados_fatura_instance is not None:
            form = DadosFaturaModelForm(request.POST, instance=dados_fatura_instance)

        if form.is_valid():
            dados = form.save(commit=False)
            dados.fatura_id = fatura
            dados.save()
            return redirect('uc_faturas', uc=uc)
        
    return render(request, 'faturas/dados.html', {'form': form, 'uc': uc})


@login_required(login_url="/login/")
def uc_faturas_deleta(request, uc, id):
    fatura = get_object_or_404(Faturas, id=id)
    res = fatura.delete()
    return redirect('uc_faturas', uc=uc)