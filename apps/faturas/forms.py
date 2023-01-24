from django import forms
from django.forms.widgets import NumberInput

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
