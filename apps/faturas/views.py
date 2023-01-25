from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UploadFaturaForm, UploadFaturaResumidaForm
from django.core.files.storage import FileSystemStorage
from apps.ETL import FaturaGrupoA4
from django.conf import settings
from django.template import loader
from django.http import HttpResponse

# Create your views here.
@login_required(login_url="/login/")
def faturas(request):
    context = {}

    if request.method == 'POST' and request.FILES['fatura']:
        # print(f'arquivo recebido: {request.FILES["fatura"]}')
        fatura = request.FILES['fatura']
        fs = FileSystemStorage()
        filename = fs.save('tmp/faturas/fatura.pdf', fatura)
        uploaded_file_url = fs.url(filename)
        print(f'filename: {filename}\nurl: {uploaded_file_url}')

        filepath = F'{settings.MEDIA_ROOT}/{filename}'
        nome = filepath.split('/')[-1].split('.')[0]
        excel_file = fs.url(f'/tmp/excel/{nome}.xlsx')
        
        print(f'caminho excel: {excel_file}')
        print(f'caminho: {filepath}')

        try:
            etl_fatura = FaturaGrupoA4(filepath)
            etl_fatura.extrair()
        except:
            html_template = loader.get_template('home/page-500.html')
            return HttpResponse(html_template.render(context, request))

        return render(request, 'faturas/upload.html', 
                        {'url_file': uploaded_file_url, 'excel_file': excel_file, 'result':'ok'})
    
    return render(request, 'faturas/upload.html')