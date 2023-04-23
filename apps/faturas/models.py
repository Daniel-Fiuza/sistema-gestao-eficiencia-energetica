from django.db import models
from apps.clientes.models import UC

# Create your models here.

def diretorio_faturas(instance, filename):
    return '{0}/{1}/{2}'.format(instance.uc_id.cliente.razao_social, instance.uc_id.numero_uc, filename)
    
class Faturas(models.Model):
    uc_id = models.ForeignKey(UC, on_delete=models.DO_NOTHING)
    fatura = models.FileField(upload_to= diretorio_faturas)
    mes_ano = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.uc_id} - {self.mes_ano}'


class DadosFaturas(models.Model):
    fatura_id = models.ForeignKey(Faturas, on_delete=models.CASCADE, blank=True, null=True)
    uc_id = models.ForeignKey(UC, on_delete=models.CASCADE, blank=True, null=True)
    mes_ano_fatura = models.DateField()
    demanda_ativa_kw = models.FloatField()
    demanda_ativa_rs = models.FloatField()
    demanda_ativa_sem_icms_kw = models.FloatField()
    demanda_ativa_sem_icms_rs = models.FloatField()
    demanda_ultrapassagem_kw = models.FloatField()
    demanda_ultrapassagem_rs = models.FloatField()
    energia_atv_forn_ponta_te_kwh = models.FloatField()
    energia_atv_forn_ponta_te_rs = models.FloatField()
    energia_atv_forn_ponta_tusd_rs = models.FloatField()
    energia_atv_forn_f_ponta_te_kwh = models.FloatField()
    energia_atv_forn_f_ponta_te_rs = models.FloatField()
    energia_atv_forn_f_ponta_tusd_rs = models.FloatField()
    adicional = models.FloatField()
    consumo_reativo_excedente_fp_kwh = models.FloatField()
    consumo_reativo_excedente_fp_rs = models.FloatField()
    consumo_reativo_excedente_np_kwh = models.FloatField()
    consumo_reativo_excedente_np_rs = models.FloatField()
    cip_ilum_pub_pref_municipal_rs = models.FloatField()
    dic_rs = models.FloatField()
    juros_moratorios_rs = models.FloatField()
    multa_rs = models.FloatField()
    icms = models.FloatField()
    pis_pasep = models.FloatField()
    cofins = models.FloatField()
    faturamento = models.FloatField()
    demanda_contratada = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'Dados Fatura {self.uc_id}  Mês: {self.mes_ano_fatura}'


