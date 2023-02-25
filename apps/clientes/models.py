from django.db import models

# Create your models here.
class Clientes(models.Model):
    razao_social = models.CharField(max_length=50)
    email = models.EmailField(max_length=75)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.razao_social



CLASSES = (
    ('1', 'A4 HOROSAZONAL VERDE - Comercial'),
    ('2', 'B3 OUTROS-CONV. - Comercial'),
)

class UC(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.DO_NOTHING, related_name='uc')
    numero_uc = models.CharField(max_length=15)
    numero_cliente = models.CharField(max_length=15, blank=True, null=True)
    classificacao = models.CharField(max_length=3, choices=CLASSES)
    cnpj = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.numero_uc} - {self.cliente}'