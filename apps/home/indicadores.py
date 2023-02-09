

class Indicadores():
    def __init__(self, uc, data_inicial=None, data_final=None) -> None:
        self.uc = uc

    def calcula_multas(self):
        pass

    def calcula_kwh_efetivo(self):
        pass

    def resultado(self):
        self.multas = self.calcula_multas()