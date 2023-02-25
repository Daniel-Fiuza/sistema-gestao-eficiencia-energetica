from django import forms
from .models import Clientes, UC, CLASSES

class CadastroClienteForm(forms.ModelForm):

    razao_social = forms.CharField(
        label='Razão Social',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Razão Social",
                "class": "form-control"
            }
        )
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Clientes
        fields = ['razao_social','email']



class CadastroUCForm(forms.ModelForm):

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
                "placeholder": "Número do Cliente",
                "class": "form-control"
            }
        )
    )

    classificacao = forms.ChoiceField( choices= CLASSES)

    cnpj = forms.CharField(
        label='CNPJ',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Cnpj",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = UC
        fields = ['numero_uc', 'numero_cliente', 'classificacao', 'cnpj']