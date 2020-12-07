from tree import Tree
from element import Element
from tabSymbols import TabSymbols

class Semantica():

    def __init__(self):
        self.pilhaEscopos = ['global']
        self.tabSymbols = TabSymbols(self.pilhaEscopos)

    def percorrerTree(self, root):
        if root:
            for soon in root.child:
                if soon.type == "declaracao_variaveis":
                    self.declaracao_variaveis(soon)
                elif soon.type == "declaracao_funcao":
                    self.declaracao_funcao(soon)
                elif soon.type == "retorna":
                    self.retorna(soon)
                elif soon.type == "atribuicao":
                    self.atribuicao(soon)
                elif soon.type == "chamada_funcao":
                    self.chamada_funcao(soon)
                elif soon.type == "escreva":
                    self.escreva(soon)
                elif soon.type == "leia":
                    self.leia(soon)
                elif soon.type == "se":
                    self.se(soon)
                elif soon.type == "repita":
                    self.repita(soon)
                elif soon.type == "até":
                    self.ate(soon)
                elif soon.type == "fim":
                    self.fim(soon)
                if not isinstance(soon, Tree):
                    return
                self.percorrerTree(soon)
        else:
            return

    def get_node_folhas_variaveis(self, soon):
        lista_values = []
        index_valor = None
        index_tipo = None
        for i in soon.child:
            if i.value != 'vazio' and len(i.child) == 0:
                lista_values.append(i)
            elif i.value != 'vazio' and len(i.child) == 1:
                lista_values.append(i)
                index_tipo = i.child[0].child[0].type
                index_valor = i.child[0].child[0].value
        return lista_values, index_valor, index_tipo

    def get_value_node_folhas(self, soon):
        lista_values = []
        for i in soon.child:
            if i.value != 'vazio':
                lista_values.append(i.value)
        return lista_values

    def fim(self, soon):
        self.pilhaEscopos.pop()

    def ate(self, soon):
        self.pilhaEscopos.pop()

    def repita(self, soon):
        self.tabSymbols.inserir_funcao(soon.type, None, None, None, None)
        expressao = soon.child[1]
        self.resolve_expressao(expressao, soon.type)

    def se(self, soon):
        self.tabSymbols.inserir_funcao(soon.type, None, None, None, None)

    def escreva(self, soon):
        if soon.child[0].type == "chamada_funcao":
            funcao = self.tabSymbols.find_funcao(soon.child[0].value)
            if funcao != None:
                funcao.used = True
            else:
                print("Erro: função '" +
                      soon.child[0].value + "' não declarada -> Linha: " + str(soon.linha))
        elif soon.child[0].type == "var":
            variavel = soon.child[0].value
            find_e = self.tabSymbols.find_elemento(variavel)
            if find_e != None:
                find_e.used = True
            else:
                print("Erro: A variavel '" +
                      soon.child[0].value + "' não declarada -> Linha: " + str(soon.linha))

    def leia(self, soon):
        if soon.child[0].type == "chamada_funcao":
            funcao = self.tabSymbols.find_funcao(soon.child[0].value)
            if funcao != None:
                funcao.used = True
            else:
                print("Erro: função '" +
                      soon.child[0].value + "' não declarada -> Linha: " + str(soon.linha))
        elif soon.child[0].type == "var":
            variavel = soon.child[0].value
            find_e = self.tabSymbols.find_elemento(variavel)
            if find_e != None:
                find_e.used = True
            else:
                print("Linha:["+str(soon.linha)+"] Erro: A variavel '" +
                      soon.child[0].value + "' não está declarada")
        else:
            print("Erro: Não foi possivel realizar a escrita -> Linha: " + str(soon.linha))

    def chamada_funcao(self, soon):
        nome = soon.value
        if nome == "principal":
            if self.pilhaEscopos[-1] != "principal":
                print("Erro: Chamada para a função principal não permitida")
            else:
                print("Aviso: Chamada recursiva para principal")
        lista_arg = []
        for arg in soon.child[0].child:
            if str(arg) != "vazio":
                lista_arg.append(arg)

        funcao = self.tabSymbols.find_funcao(nome)
        if(funcao != None):
            if (len(funcao.lista_paramentros) > len(lista_arg)):
                print("Erro: Chamada à função '" + nome +
                      "' com número de parâmetros menor que o declarado")
            elif (len(funcao.lista_paramentros) < len(lista_arg)):
                print("Erro: Chamada à função '" + nome +
                      "' com número de parâmetros maior que o declarado")
            funcao.used = True
        else:
            if nome != "principal":
                print("Erro: Chamada da função '" +
                      nome + "' que não foi declarada")

    def atribuicao(self, soon):
        variavel = soon.child[0]
        index = None
        if len(variavel.child) > 0:
            index = variavel.child[0].child[0]
        find_e = self.tabSymbols.find_elemento(variavel.value)
        if find_e == None:
            print("Erro: A variavel '" +
                  variavel.value + "'não declarada" + str(variavel.linha))
        else:
            find_e.used = True
            find_e.inicializado = True
            if index != None:
                if index.type == "var":
                    e = self.tabSymbols.find_elemento(index.value)
                    if e:
                        e.used = True
                        index = e.valor
                        if int(float(index)) != None and find_e.indice < int(float(index)):
                            print("Erro: O vetor '" + variavel.value +
                                  "' que deseja atribuir, esta fora do range declarado")
                else:
                    expressao = self.resolve_expressao(
                        soon.child[1], self.pilhaEscopos[-1])
                    tipo = expressao
                    index = int(float(index))
                    if index < find_e.indice:
                        find_e.used = True
                        if find_e.tipo != tipo:
                            print("Aviso: A variavel " + find_e.nome + " é do tipo " + find_e.tipo +
                                  " mas esta recebendo um valor do tipo " + tipo + " -> Linha: " + str(soon.linha))
            else:
                try:
                    soon.child[1].child[0].type == "chamada_funcao"
                    find_f = self.tabSymbols.find_funcao(soon.child[1].child[0].value)
                    tipo = find_f.tipo_retorno
                    find_e.used = True
                    if find_e.tipo != tipo:
                        print("Aviso: A variavel " + find_e.nome + " é do tipo " + find_e.tipo +
                            " mas esta recebendo um valor do tipo " + tipo + " -> Linha: " + str(soon.linha))
                except:
                    expressao = self.resolve_expressao(soon.child[1], self.pilhaEscopos[-1])
                    tipo = expressao
                    find_e.used = True
                    if find_e.tipo != tipo:
                        print("Aviso: A variavel " + str(find_e.nome) + " é do tipo " + str(find_e.tipo) +
                            " mas esta recebendo um valor de tipo " + str(tipo) + " -> Linha: " + str(soon.linha))
    
    def str_or_int(self, s):
        try:
            int(s)
            return "inteiro"
        except ValueError:
            return "varivael"

    def retorna_tipo_node(self, no):
        if str(type(no.value)) == "<class 'str'>":
            if self.str_or_int(no.value) == "inteiro":
                return "inteiro"
            else:
                elemento = self.tabSymbols.find_elemento(no.value)
                if elemento != None:
                    return elemento.tipo
                else:
                    print("Erro: A variavel '" +
                          no.value + "' não está declarada")
                    exit(1)
        elif str(type(no.value)) == "<class 'float'>":
            return "flutuante"
        elif str(type(no.value)) == "<class 'int'>":
            return "inteiro"

    def resolve_expressao(self, soon, funcao):
        if len(soon.child) == 1:
            funcao_escopo = self.tabSymbols.find_funcao(funcao)
            if soon.child[0].type == "var":
                variavel = self.tabSymbols.find_elemento(soon.child[0].value)
                if variavel != None and variavel.parametro == True:
                    variavel.used = True
                    tipo_meio = self.retorna_tipo_node(
                        soon.child[0])
                    return tipo_meio
                elif variavel != None and variavel.parametro == False:
                    variavel.used = True
                    tipo_meio = self.retorna_tipo_node(
                        soon.child[0])
                    return tipo_meio
                else:
                    print("Erro: A variavel " +
                          soon.child[0].value + " ainda não foi declarada -> Linha: " + str(soon.child[0].linha))
            else:
                tipo_meio = self.retorna_tipo_node(
                    soon.child[0])
                return tipo_meio
        if len(soon.child) == 3:
            funcao_escopo = self.tabSymbols.find_funcao(funcao)
            soon_esquerda = soon.child[0]
            operador = soon.child[1]
            soon_direita = soon.child[2]
            tipo_direita = self.retorna_tipo_node(
                soon_direita)
            tipo_esquerda = self.retorna_tipo_node(
                soon_esquerda)
            if tipo_direita != tipo_esquerda:
                print("Aviso: A expressão com o operador '" + str(operador.value) +
                      "' utilizando " + tipo_direita + " e " + tipo_esquerda + " -> Linha: " + str(operador.linha))
                return tipo_direita
            else:
                if tipo_esquerda != funcao_escopo.tipo_retorno and funcao_escopo.tipo_retorno != None:
                    return funcao_escopo.tipo_retorno
                else:
                    return tipo_direita

    def retorna(self, soon):
        funcao = self.tabSymbols.find_funcao(self.pilhaEscopos[-1])
        if funcao.escopo_pai != "global":
            while funcao.escopo_pai != "global":
                funcao = self.tabSymbols.find_funcao(
                    funcao.escopo_pai)

        if funcao != None:
            expressao = self.resolve_expressao(
                soon.child[0], funcao.nome)
            tipo = expressao
            if str(tipo) != str(funcao.tipo_retorno):
                if(funcao.tipo_retorno == "vazio"):
                    print("Erro: Função " +
                          str(funcao.nome) + " do tipo vazio retorna " + str(tipo) + "Linha: " + str(soon.linha))
                else:
                    print("Erro: Função '"+str(funcao.nome)+"' do tipo '" +
                          str(funcao.tipo_retorno)+"' retorna '"+str(tipo)+"'")
                    funcao.foi_retornada = True
            elif funcao.tipo_retorno == tipo:
                funcao.foi_retornada = True
            else:
                print("Erro: A função esta retornando um tipo diferente do declarado")
        else:
            print("Erro: O progama esta retornado algo fora de um escopo valido")

    def declaracao_funcao(self, soon):
        if soon.child[0].type == "tipo":
            tipo = soon.child[0].value
            nome = soon.child[1].value
            lista_paramentros = []
            self.declara_funcao_na_tabela_de_simbolos(
                nome, lista_paramentros, tipo, soon)
            for param in soon.child[1].child[0].child:
                for tipo in param.child:
                    parametro = True
                    self.tabSymbols.inserir_elemento(
                        param.value, tipo.value, None, True, nome, parametro)
                    lista_paramentros.append(param.value)
            if nome == "principal":
                self.tabSymbols.principal = True
        else:
            tipo = "vazio"
            nome = soon.child[0].value
            lista_paramentros = []
            self.declara_funcao_na_tabela_de_simbolos(
                nome, lista_paramentros, tipo, soon)
            for param in soon.child[0].child[0].child:
                for tipo in param.child:
                    parametro = True
                    self.tabSymbols.inserir_elemento(
                        param.value, tipo.value, None, True, nome, parametro)
                    lista_paramentros.append(param.value)
            if nome == "principal":
                self.tabSymbol.principal = True

    def declara_funcao_na_tabela_de_simbolos(self, nome, lista_paramentros, tipo, no):
        if self.tabSymbols.find_funcao(nome) != None:
            print("Aviso: Função " +
                  nome + " já declarada anteriormente -> Linha: " + no.linha)
        else:
            self.tabSymbols.inserir_funcao(
                nome, str(tipo), False, lista_paramentros, False, no.linha)

    def declara_variaveis_na_tabela_de_simbolos(self, lista_variaveis, tipo, index):
        for variavel in lista_variaveis:
            if(self.tabSymbols.find_elemento(variavel.value) != None):
                print("Aviso: Variável " +
                      variavel.value + " já declarada anteriormente Linha: " + str(variavel.linha))
            elif index != None:
                index = int(float(index))
                v = []
                for i in range(int(float(index))):
                    v.append('null')
                self.tabSymbols.inserir_elemento(
                    variavel.value, tipo, index, False, self.pilhaEscopos[-1], False, variavel.linha)
            else:
                self.tabSymbols.inserir_elemento(
                    variavel.value, tipo, index, False, self.pilhaEscopos[-1], False, variavel.linha)

    def declaracao_variaveis(self, soon):
        resultado = self.get_node_folhas_variaveis(soon.child[1])
        lista_variaveis = resultado[0]
        index_valor = resultado[1]
        index_tipo = resultado[2]
        tipo = soon.child[0].value
        if index_tipo != "numero_int" and index_valor != None:
            print("Erro: índice de array " +
                  str(lista_variaveis[0].value) + " não é um inteiro -> Linha: " + str(lista_variaveis[0].linha))
        else:
            self.declara_variaveis_na_tabela_de_simbolos(
                lista_variaveis, tipo, index_valor)
    
    def verificacoes(self):
        if(self.tabSymbols.principal == False):
            print("Erro: Função principal não declarada")
        self.tabSymbols.conferir_variaveis_usadas()
        self.tabSymbols.conferir_funcoes_declaradas()
    
    def printTabSymbols(self):
        self.tabSymbols.print_tabela_simbolos()
        self.tabSymbols.print_tabela_funcoes()
        self.tabSymbols.print_pilha()