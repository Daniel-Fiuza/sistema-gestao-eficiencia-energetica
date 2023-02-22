from django.contrib import admin
from .models import Faturas, DadosFaturas

# Register your models here.
admin.site.register(Faturas)
admin.site.register(DadosFaturas)