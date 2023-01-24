from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UploadFaturaForm

# Create your views here.
@login_required(login_url="/login/")
def faturas(request):
    context = {}

    if request.method == 'POST':
        form = UploadFaturaForm(request.POST, request.FILES)
        print(f'POST: {request.POST}\nFILE: {request.FILES}')
        if form.is_valid():
            print(f'arquivo recebido: {request.POST["file"]}')
            # handle_uploaded_file(request.FILES['file'])
            return render(request, 'home/faturas.html', {'form': form, 'result':'ok'})
    else:
        form = UploadFaturaForm()
    return render(request, 'home/faturas.html', {'form': form})