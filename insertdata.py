import datetime
from apps.clientes.models import UC

fields = {
    'uc_id': UC.objects.get(id=1),
    'mes_ano_fatura': datetime.date(2022,4,1),
    'demanda_ativa_kw': 215.88,
    'demanda_ativa_rs': 5890.98,
    'demanda_ativa_sem_icms_kw': 0,
    'demanda_ativa_sem_icms_rs': 0,
    'demanda_ultrapassagem_kw': 16,
    'demanda_ultrapassagem_rs': 866.65,
    'energia_atv_forn_ponta_te_kwh': 4702,
    'energia_atv_forn_ponta_te_rs': 2668.53,
    'energia_atv_forn_ponta_tusd_rs': 8068.27,
    'energia_atv_forn_f_ponta_te_kwh': 39845,
    'energia_atv_forn_f_ponta_te_rs': 13967.04,
    'energia_atv_forn_f_ponta_tusd_rs': 3438.34,
    'adicional': 9066.01,
    'consumo_reativo_excedente_fp_kwh': 124,
    'consumo_reativo_excedente_fp_rs': 45.69,
    'consumo_reativo_excedente_np_kwh': 4,
    'consumo_reativo_excedente_np_rs': 1.43,
    'cip_ilum_pub_pref_municipal_rs': 323.83,
    'dic_rs': 0,
    'juros_moratorios_rs': 0,
    'multa_rs': 0,
    'icms': 11883.46,
    'pis_pasep': 250.57,
    'cofins': 1169.47,
    'faturamento': 44336.77,
    'demanda_contratada': 200
}