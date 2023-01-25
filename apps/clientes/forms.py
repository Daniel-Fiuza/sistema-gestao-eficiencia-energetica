from django import forms
from .models import Clientes

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