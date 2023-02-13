from apps.faturas.models import DadosFaturas
from pandas.tseries.offsets import DateOffset
import pandas as pd
import datetime

class Indicadores():
    def __init__(self, uc, filtro=None) -> None:
        self.uc = uc
        self.filtro = self.converte_filtro(filtro)


    def converte_filtro(self, filtro):
        if filtro == '1 mes':
            return 0
        if filtro == '3 meses':
            return 3
        if filtro == '6 meses':
            return 6
        if filtro == '1 ano':
            return 12


    def calcula_multas(self):
        df = pd.DataFrame(list(DadosFaturas.objects.all().values()))
        df['mes_ano_fatura'] = pd.to_datetime(df['mes_ano_fatura'], format='%Y-%m-%d')
        df.sort_values(by=['mes_ano_fatura'], ascending=False, inplace=True)
        df = df.loc[df['mes_ano_fatura'] >= (df['mes_ano_fatura'].iloc[0] - DateOffset(months=self.filtro))]

        df['multas_reativo'] = df['consumo_reativo_excedente_fp_rs'] + df['consumo_reativo_excedente_np_rs']
        df_filtrado = df[['mes_ano_fatura','demanda_ultrapassagem_rs','multas_reativo','multa_rs']]
        
        print(f'df filtrado:\n {df_filtrado}')
        # df_filtrado.to_dict('index')
        return df_filtrado


    def calcula_kwh_efetivo(self):
        pass

    def resultado(self):
        self.multas = self.calcula_multas()