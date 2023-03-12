from django import forms
from .models import Faturas
from django.forms.widgets import NumberInput
import datetime


class UploadFaturaResumidaForm(forms.Form):
    fatura = forms.FileField(
        label='Fatura',
        widget=forms.FileInput(
            attrs={
                "placeholder": "Faça o upload da fatura",
                "class": "form-control"
            }
    ))


class CustomDateField(forms.DateField):
    def to_python(self, value):
        # add day in date string. value example: 2023-03
        value += '-01'

        if value in self.empty_values:
            return None
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value
        return super().to_python(value)
    

class CadastroFaturaModelForm(forms.ModelForm):
    fatura = forms.FileField(
        label='Fatura',
        widget=forms.FileInput(
            attrs={
                "placeholder": "Faça o upload da fatura",
                "class": "form-control"
            }
    ))

    mes_ano = CustomDateField(
        label='Mês de Referência',
        widget=forms.DateInput(attrs={'type': 'month'}))

    class Meta:
        model = Faturas
        fields = ['fatura', 'mes_ano']


class UploadFaturaForm(forms.Form):
    
    numero_uc = forms.CharField(
        label='Número da UC',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Número da UC",
                "class": "form-control"
            }
        )
    )

    numero_cliente = forms.CharField(
        label='Número do Cliente',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Número do cliente",
                "class": "form-control"
            }
        )
    )

    razao_social = forms.CharField(
        label='Razão Social',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Razão Social",
                "class": "form-control"
            }
        )
    )

    CLASSIFICACAO_UC = [
        ('A4', 'A4 HOROSAZONAL VERDE'),
        ('B3', 'B3 OUTROS-CONV.'),
    ]
    classificacao_uc = forms.ChoiceField(
        label='Classificação da UC',
        choices=CLASSIFICACAO_UC)

    mes_referencia = forms.DateField(
        label='Mês de Referência',
        widget=NumberInput(attrs={'type': 'month'}))

    fatura = forms.FileField(
        label='Fatura',
        widget=forms.FileInput(
            attrs={
                "placeholder": "Fatura",
                "class": "form-control"
            }
    ))
