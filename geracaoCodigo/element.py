class Element():
    def __init__(self, nome, escopo, tipo, indice, used, parametro, linha=None, inicializado=None):
        self.nome = nome
        self.escopo = escopo
        self.tipo = tipo
        self.used = used
        self.indice = indice
        self.parametro = parametro
        self.linha = linha
        self.inicializado = inicializado

    def set_uso(self, elemento, usado):
        if(elemento):
            elemento.used = usado
        else:
            print("Erro: Variavel ainda não declarada")

    def get_tipo(self, elemento):
        return elemento.tipo

    def set_tipo(self, elemento, tipo):
        elemento.tipo = tipo