from django.db import models
from apps.clientes.models import UC

# Create your models here.

def diretorio_faturas(instance, filename):
    return 'apps/media/faturas/{0}/{1}/{2}'.format(instance.uc_id.cliente.razao_social, instance.uc_id.numero_uc, filename)
    
class Faturas(models.Model):
    uc_id = models.ForeignKey(UC, on_delete=models.DO_NOTHING)
    fatura = models.FileField(upload_to= diretorio_faturas)
    mes_ano = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.uc_id} - {self.mes_ano}'