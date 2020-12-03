class FunctionData():
    def __init__(self, nome, tipo_retorno, lista_paramentros, foi_retornada, escopo, used, escopo_pai, linha=None):
        self.nome = nome
        self.tipo_retorno = tipo_retorno
        self.lista_paramentros = lista_paramentros
        self.escopo = escopo
        self.escopo_pai = escopo_pai
        self.foi_retornada = foi_retornada
        self.used = used
        self.linha = linha