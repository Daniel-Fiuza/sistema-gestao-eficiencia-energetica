from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Clientes, UC
from .forms import CadastroClienteForm

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