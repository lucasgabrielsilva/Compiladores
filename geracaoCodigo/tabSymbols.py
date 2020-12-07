from element import Element
from functionData import FunctionData

class TabSymbols():

    def __init__(self, pilhaEscopos):
        self.lista_elementos = []
        self.lista_funcoes = []
        self.pilhaEscopos = pilhaEscopos
        self.principal = False

    def pega_lista_funcoes(self):
        return self.lista_funcoes

    def inserir_elemento(self, nome, tipo, indice, used, Escopo, parametro, linha=None):
        self.lista_elementos.append(
            Element(nome, Escopo, tipo, indice, used, parametro, linha, False))

    def inserir_funcao(self, nome, tipo_retorno, foi_retornada, lista_paramentros, used, linha=None):
        escopo_pai = self.pilhaEscopos[-1]
        self.pilhaEscopos.append(nome)
        self.lista_funcoes.append(FunctionData(
            nome, tipo_retorno, lista_paramentros, foi_retornada, self.pilhaEscopos[-1], used, escopo_pai, linha))

    def find_elemento(self, var):
        for escopo in self.pilhaEscopos:
            for elemento in self.lista_elementos:
                if elemento.nome == str(var) and elemento.escopo == escopo:
                    return elemento
        return None

    def find_funcao(self, nome):
        for funcao in self.lista_funcoes:
            if funcao.nome == nome:
                return funcao
        return None

    def print_tabela_funcoes(self):
        print("\nTABELA DE FUNCOES")
        for f in self.lista_funcoes:
            if f.escopo_pai != "global":
                print("     + ----> Nome: " + f.nome + " Escopo: " +
                      str(f.escopo) + " Escopo_PAI: " + str(f.escopo_pai))
            else:
                print("Nome: " + f.nome + " Lista_Parametros: " + str(f.lista_paramentros) + " Tipo_Retorno: " + str(f.tipo_retorno) +
                      " Escopo: " + str(f.escopo) + " Escopo_PAI: " + str(f.escopo_pai) + " Foi_Retornada: " + str(f.foi_retornada))

    def conferir_variaveis_usadas(self):
        if self.lista_elementos:
            for elemento in self.lista_elementos:
                if elemento.used == False:
                    print(" Aviso: Variável '" +
                          str(elemento.nome) + "' declarada e não utilizada -> Linha:" + str(elemento.linha))
                elif elemento.used == True and elemento.inicializado == False and elemento.parametro == False:
                    print("Aviso: Variável '" +
                          str(elemento.nome) + "' não inicializada -> Linha" + str(elemento.linha))

    def conferir_funcoes_declaradas(self):
        for f in self.lista_funcoes:
            if(f.foi_retornada == False):
                if f.tipo_retorno != "vazio" and f.foi_retornada == False:
                    print("Erro: Função '" + str(f.nome) + "' deveria retornar '" +
                          str(f.tipo_retorno) + "', mas retorna vazio")
            if(f.used == False and f.nome != "principal"):
                print("Aviso: Função '"+str(f.nome) +
                      "' declarada, mas não utilizada")
    
    def print_pilha(self):
        print("\nPILHA DE ESCOPOS")
        for elemento in self.pilhaEscopos:
            print(elemento)

    def print_tabela_simbolos(self):
        print("\nTABELA DE SIMBOLOS")
        for e in self.lista_elementos:
            if(e.indice):
                print("Tipo: " + str(e.tipo) + " Nome: " + str(e.nome) + " Indice: " +
                      str(e.indice) + " Escopo: " + str(e.escopo) + " Usada: " + str(e.used))
            else:
                print("Tipo: " + str(e.tipo) + " Nome: " + str(e.nome) +
                      " Escopo: " + str(e.escopo) + " Usada: " + str(e.used))