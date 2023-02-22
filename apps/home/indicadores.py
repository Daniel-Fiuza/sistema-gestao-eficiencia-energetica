from apps.faturas.models import DadosFaturas
from pandas.tseries.offsets import DateOffset
import pandas as pd
from dataclasses import dataclass
import json
import locale

locale.setlocale(locale.LC_ALL, '')

@dataclass
class FormatChart:
    labels: str
    datasets: list

@dataclass
class FormatPieChart:
    labels: list
    data: list

@dataclass
class CardsIndicadores:
    total_pago: str = '0.0'
    multas_pagas: str = '0.0'
    kwh_efetivo: str = '0.0'
    meta_economia: str = '15,00 %'

TIME_FILTER = {
    '1 Ano': 12,
    '6 Meses': 6,
    '3 Meses': 3,
    '1 Mês': 0,
}


class Indicadores():
    def __init__(self, uc, filtro=None) -> None:
        self.uc = uc
        self.filtro = self.converte_filtro(filtro)
        self.df = self.obtem_dados()
        self.card = CardsIndicadores()


    def efetua_calculos(self):
        self.multas = self.calcula_multas()
        self.ult_demanda = self.calcula_ult_demanda()
        self.kwh_efetivo = self.calcula_kwh_efetivo()
        self.dist_gastos = self.calcula_distribuicao_gastos()
        self.hp_hfp = self.calcula_hp_hfp()

        
    def obtem_dados(self):
        df = pd.DataFrame(list(DadosFaturas.objects.filter(uc_id__numero_uc = self.uc).values()))
        if len(df) == 0:
            print(f'Dados da uc {self.uc} inexistentes.')
            return []
        df['mes_ano_fatura'] = pd.to_datetime(df['mes_ano_fatura'], format='%Y-%m-%d')
        df.sort_values(by=['mes_ano_fatura'], ascending=False, inplace=True)
        df = self.filtra_por_data(df, self.filtro)
        return df


    def checa_dados(self):
        ''' Verifica se existem dados no banco, caso não exista retorna um dataset vazio. Isso é utilizado para não quebrar o padrão de retorno dos métodos de cálculos de indicadores. '''
        if len(self.df) == 0:
            return False, {'labels': [], 'datasets': []}
        return True, None


    def converte_filtro(self, filtro):
        global TIME_FILTER

        try:
            return TIME_FILTER[filtro]
        except:
            raise KeyError("Nome do filtro não identificado")


    def filtra_por_data(self, df, filtro):
        return df.loc[df['mes_ano_fatura'] >= (df['mes_ano_fatura'].iloc[0] - DateOffset(months=filtro))]


    def calcula_multas(self):
        existe, data = self.checa_dados()
        if (existe is False):
            return data

        df_indicador = self.df.copy()
        df_indicador['mes_ano_fatura'] = df_indicador['mes_ano_fatura'].dt.strftime('%m-%Y')

        df_indicador['multas_reativo'] = df_indicador['consumo_reativo_excedente_fp_rs'] + df_indicador['consumo_reativo_excedente_np_rs']
        df_indicador[['demanda_ultrapassagem_rs','multas_reativo','multa_rs']] = df_indicador[['demanda_ultrapassagem_rs','multas_reativo','multa_rs']].round(2)
        
        multas_pagas = df_indicador['demanda_ultrapassagem_rs'].sum() + df_indicador['multas_reativo'].sum() + df_indicador['multa_rs'].sum()
        self.card.multas_pagas = locale.currency(multas_pagas, grouping=True)

        df_filtrado = df_indicador[['mes_ano_fatura','demanda_ultrapassagem_rs','multas_reativo','multa_rs']]
        df_filtrado = df_filtrado.sort_values(by=['mes_ano_fatura'])
        data_dict = df_filtrado.to_dict('list')
        
        format = FormatChart(
            labels= 'mes_ano_fatura',
            datasets= ['demanda_ultrapassagem_rs','multas_reativo','multa_rs']
        )
        data_result = self.format_to_chart(data_dict, format)

        return json.dumps(data_result)


    def calcula_ult_demanda(self):
        existe, data = self.checa_dados()
        if (existe is False):
            return data

        df_indicador = self.df.copy()
        df_indicador['mes_ano_fatura'] = df_indicador['mes_ano_fatura'].dt.strftime('%m-%Y')
    
        df_indicador[['demanda_ativa_kw','demanda_contratada']] = df_indicador[['demanda_ativa_kw','demanda_contratada']].round(2)
        df_filtrado = df_indicador[['mes_ano_fatura','demanda_ativa_kw','demanda_contratada']]

        df_filtrado = df_filtrado.sort_values(by=['mes_ano_fatura'])
        data_dict = df_filtrado.to_dict('list')
        
        format = FormatChart(
            labels= 'mes_ano_fatura',
            datasets= ['demanda_ativa_kw','demanda_contratada']
        )
        data_result = self.format_to_chart(data_dict, format, offset_color=3, type_chart=['bar', 'line'])

        return json.dumps(data_result)


    def calcula_kwh_efetivo(self):
        existe, data = self.checa_dados()
        if (existe is False):
            return data

        df_indicador = self.df.copy()
        df_indicador['mes_ano_fatura'] = df_indicador['mes_ano_fatura'].dt.strftime('%m-%Y')
        
        df_indicador['total_consumo_mensal'] = df_indicador['energia_atv_forn_ponta_te_kwh'] + \
                                               df_indicador['energia_atv_forn_f_ponta_te_kwh']
        df_indicador['fatura_rs'] = df_indicador['demanda_ativa_rs'] + df_indicador['demanda_ativa_sem_icms_rs'] + df_indicador['demanda_ultrapassagem_rs'] + df_indicador['energia_atv_forn_ponta_te_rs'] + df_indicador['energia_atv_forn_ponta_tusd_rs'] + df_indicador['energia_atv_forn_f_ponta_te_rs'] + df_indicador['energia_atv_forn_f_ponta_tusd_rs'] + df_indicador['adicional'] + df_indicador['consumo_reativo_excedente_fp_rs'] + df_indicador['consumo_reativo_excedente_np_rs'] + df_indicador['cip_ilum_pub_pref_municipal_rs'] + df_indicador['dic_rs']
        df_indicador['preco_medio'] = df_indicador['fatura_rs'] / df_indicador['total_consumo_mensal']
        
        df_indicador['preco_medio'] = df_indicador['preco_medio'].round(2)
        df_filtrado = df_indicador[['mes_ano_fatura', 'preco_medio']]

        kwh_efetivo = df_filtrado['preco_medio'].mean()
        self.card.kwh_efetivo = locale.currency(kwh_efetivo, grouping=True)

        df_filtrado = df_filtrado.sort_values(by=['mes_ano_fatura'])
        data_dict = df_filtrado.to_dict('list')

        format = FormatChart(
            labels= 'mes_ano_fatura',
            datasets= ['preco_medio']
        )
        data_result = self.format_to_chart(data_dict, format, offset_color=2)

        return json.dumps(data_result)


    def calcula_distribuicao_gastos(self):
        existe, data = self.checa_dados()
        if (existe is False):
            return data

        demanda_rs = self.df['demanda_ativa_rs'].sum() + self.df['demanda_ativa_sem_icms_rs'].sum()
        ultrapassagem_rs = self.df['demanda_ultrapassagem_rs'].sum()
        consumo_rs = self.df['energia_atv_forn_ponta_te_rs'].sum() + self.df['energia_atv_forn_ponta_tusd_rs'].sum() + self.df['energia_atv_forn_f_ponta_te_rs'].sum() + self.df['energia_atv_forn_f_ponta_tusd_rs'].sum()
        reativo_rs = self.df['consumo_reativo_excedente_fp_rs'].sum() + self.df['consumo_reativo_excedente_np_rs'].sum()
        adicional_rs = self.df['adicional'].sum()
        iluminacao_publica_rs = self.df['cip_ilum_pub_pref_municipal_rs'].sum()
        atraso_pagamento_rs = self.df['juros_moratorios_rs'].sum() + self.df['multa_rs'].sum()
        
        indicadores = [demanda_rs, ultrapassagem_rs, consumo_rs, reativo_rs, adicional_rs, iluminacao_publica_rs, atraso_pagamento_rs]
        indicadores = [round(indicador, 2) for indicador in indicadores]
        total_value = sum(indicadores)
        percentage = [round(indicador*100/total_value, 2) for indicador in indicadores]

        total_pago = round(total_value, 2)
        self.card.total_pago = locale.currency(total_pago, grouping=True)

        format = FormatPieChart(
            labels= ['Demanda', 'Ultrapassagem', 'Consumo', 'Reativo', 'Adicional', 'Ilum. Publica', 'Atraso Pagamento'],
            data= percentage
        )
        data_result = self.format_to_pie_chart(format)

        return json.dumps(data_result)


    def calcula_hp_hfp(self):
        existe, data = self.checa_dados()
        if (existe is False):
            return data

        hp = self.df['energia_atv_forn_ponta_te_rs'].sum() + self.df['energia_atv_forn_ponta_tusd_rs'].sum()
        hfp = self.df['energia_atv_forn_f_ponta_te_rs'].sum() + self.df['energia_atv_forn_f_ponta_tusd_rs'].sum()

        indicadores = [hp, hfp]
        indicadores = [round(indicador, 2) for indicador in indicadores]
        total_value = sum(indicadores)
        
        percentage = [round(indicador*100/total_value, 2) for indicador in indicadores]

        format = FormatPieChart(
            labels= ['HP', 'HFP'],
            data= percentage
        )
        data_result = self.format_to_pie_chart(format, offset_color=2)

        return json.dumps(data_result)


    def format_to_pie_chart(self, format: FormatChart, offset_color=0):
        data_formated = {}
        data_formated["labels"] = format.labels
        data_formated["datasets"] = []

        dataset = {
            'label': 'Distribuicao de Gastos',
            'data': format.data,
        }
        data_formated["datasets"].append(dataset)

        return data_formated


    def format_to_chart(self, data, format: FormatChart, offset_color=0, type_chart=[]):
        # colors = ["#ff6384", "#36a2eb", "#cc65fe", "#ffce56", "green", "brown"]
        colors = ['#003f5c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600', '#FFB1C1']
        data_formated = {}
        data_formated["labels"] = data[format.labels]
        data_formated["datasets"] = []

        for idx, field in enumerate(format.datasets):
            dataset = {
                "label": field,
                "data": data[field],
                "borderColor": colors[idx + offset_color],
                "backgroundColor": colors[idx + offset_color],
            }
            if len(type_chart) > 0:
                dataset['type'] = type_chart[idx]
                if type_chart[idx] == 'line':
                    del dataset['backgroundColor']

            data_formated["datasets"].append(dataset)

        return data_formated