import sys
import ply.yacc as yacc
from lexica import Lexica
from tree import Tree

class Sintatica:

    def __init__(self, data, tokens):
        self.tokens = tokens
        self.precedencia = (
            ('left', 'IGUAL', 'MAIOR_IGUAL', 'MAIOR', 'MENOR_IGUAL', 'MENOR'),
            ('left', 'MAIS', 'MENOS'),
            ('left', 'MULTIPLICACAO', 'DIVISAO'),
        )
        self.ast = yacc.yacc(debug=True, module=self, optimize=False).parse(data)

    def p_programa(self, p):
        """
            programa : lista_declaracoes
        """
        p[0] = Tree('programa', [p[1]])

    def p_lista_declaracoes(self, p):
        """
            lista_declaracoes : lista_declaracoes declaracao
                | declaracao
        """
        if(len(p) == 3):
            p[0] = Tree('lista_declaracoes', [p[1], p[2]])
        else:
            p[0] = Tree('lista_declaracoes', [p[1]])

    def p_declaracao(self, p):
        """
            declaracao : declaracao_variaveis
                | inicializacao_variaveis
                | declaracao_funcao
        """
        p[0] = Tree('declaracao', [p[1]], p.lineno(1))

    def p_declaracao_variaveis(self, p):
        """
            declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis
        """
        p[0] = Tree('declaracao_variaveis', [p[1], p[3]], p[2])

    def p_inicializacao_variaveis(self, p):
        """
            inicializacao_variaveis : atribuicao
        """
        p[0] = Tree('inicializacao_variaveis', [p[1]])

    def p_lista_variaveis(self, p):
        """
            lista_variaveis : lista_variaveis VIRGULA var
                | var
        """
        if(len(p) == 4):
            p[0] = Tree('lista_variaveis', [p[1], p[3]])
        elif(len(p) == 2):
            p[0] = Tree('lista_variaveis', [p[1]])

    def p_var(self, p):
        """
            var : ID
                | ID indice
        """
        if(len(p) == 2):
            h = Tree('ID', [], p[1], p.lineno(1))
            p[0] = Tree('var', [h], p[1], p.lineno(1))
        elif(len(p) == 3):
            p[0] = Tree('var', [p[2]], p[1], p.lineno(1))

    def p_indice(self, p):
        """
            indice : indice ABRE_COLCHETE expressao FECHA_COLCHETE
                | ABRE_COLCHETE expressao FECHA_COLCHETE
        """
        if(len(p) == 5):
            p[0] = Tree('indice', [p[1], p[3]])
        elif(len(p) == 4):
            p[0] = Tree('indice', [p[2]])

    def p_inteiro(self, p):
        """
            tipo : INTEIRO
        """
        p[0] = Tree('inteiro', [], p[1])

    def p_flutuante(self, p):
        """
            tipo : FLUTUANTE
        """
        p[0] = Tree('flutuante', [], p[1])

    def p_declaracao_funcao(self, p):
        """
            declaracao_funcao : tipo cabecalho
                | cabecalho
        """
        if(len(p) == 3):
            p[0] = Tree('declaracao_funcao', [p[1], p[2]], p.lineno(2))
        elif(len(p) == 2):
            p[0] = Tree('declaracao_funcao', [p[1]], p.lineno(1))

    def p_cabecalho(self, p):
        """
            cabecalho : ID ABRE_PARENTESE lista_parametros FECHA_PARENTESE corpo FIM
        """
        p[0] = Tree('cabecalho', [p[3], p[5]], p[1])

    def p_lista_parametros(self, p):
        """
            lista_parametros : lista_parametros VIRGULA parametro
                | parametro
                | vazio
        """
        if(len(p) == 4):
            p[0] = Tree('lista_parametros', [p[1], p[3]])
        elif(len(p) == 2):
            p[0] = Tree('lista_parametros', [p[1]])

    def p_parametro(self, p):
        """
            parametro : tipo DOIS_PONTOS ID
                | parametro ABRE_COLCHETE FECHA_COLCHETE
        """
        p[0] = Tree('parametro', [p[1]], p[3])
        p[0] = Tree('parametro', [p[1]])

    def p_corpo(self, p):
        """
            corpo : corpo acao
                | vazio
        """
        if(len(p) == 3):
            p[0] = Tree('corpo', [p[1], p[2]])
        elif(len(p) == 2):
            p[0] = Tree('corpo', [p[1]])

    def p_acao(self, p):
        """
            acao : expressao
                | declaracao_variaveis
                | se
                | repita
                | leia
                | escreva
                | retorna
        """
        p[0] = Tree('acao', [p[1]])

    def p_se(self, p):
        """
            se : SE expressao ENTAO corpo FIM
                | SE expressao ENTAO corpo SENAO corpo FIM
                | SE ABRE_PARENTESE expressao FECHA_PARENTESE ENTAO corpo SENAO corpo FIM
        """
        if(len(p) == 6):
            p[0] = Tree('se', [p[2], p[4], Tree(type_node=p[5])])
        elif(len(p) == 8):
            p[0] = Tree('se', [p[2], p[4], p[6], Tree(type_node=p[7])])
        else:
            p[0] = Tree('se', [p[3],p[6],p[8]])

    def p_se2(self, p):
        """
		    se : SE ABRE_PARENTESE expressao FECHA_PARENTESE ENTAO corpo FIM
		"""
        p[0] = Tree('se', [p[3], p[6]])

    def p_repita(self, p):
        """
            repita : REPITA corpo ATE expressao
                | REPITA corpo ATE ABRE_PARENTESE expressao FECHA_PARENTESE
        """
        if(len(p) == 5):
            p[0] = Tree('repita', [p[2], p[4]])
        elif(len(p) == 7):
            p[0] = Tree('repita', [p[2], p[5]])

    def p_atribuicao(self, p):
        """
            atribuicao : var ATRIBUICAO expressao
        """
        if(len(p)):
            p[0] = Tree('atribuicao', [p[1], p[3]], p[2], p.lineno(2))

    def p_leia(self, p):
        """
            leia : LEIA ABRE_PARENTESE ID FECHA_PARENTESE
        """
        if(len(p)):
            p[0] = Tree('leia', [], p[3],p.lineno(1))

    def p_escreva(self, p):
        """
            escreva : ESCREVA ABRE_PARENTESE expressao FECHA_PARENTESE
        """
        p[0] = Tree('escreva', [p[3]],p.lineno(1))

    def p_retorna(self, p):
        """
            retorna : RETORNA ABRE_PARENTESE expressao FECHA_PARENTESE
        """
        p[0] = Tree('retorna', [p[3]], p.lineno(1))

    def p_expressao(self, p):
        """expressao : expressao_logica
            | atribuicao
        """
        p[0] = Tree('expressao', [p[1]])

    def p_expressao_logica(self, p):
        """expressao_logica : expressao_simples
                | expressao_logica operador_logico expressao_simples
        """
        if(len(p) == 2):
            p[0] = Tree('expressao_logica', [p[1]])
        else:
            p[0] = Tree('expressao_logica', [p[1], p[2], p[3]])

    def p_expressao_simples(self, p):
        """
            expressao_simples : expressao_aditiva
                | expressao_simples operador_relacional expressao_aditiva
        """
        if(len(p) == 2):
            p[0] = Tree('expressao_simples', [p[1]])
        elif(len(p) == 4):
            p[0] = Tree('expressao_simples', [p[1], p[2], p[3]])

    def p_expressao_aditiva(self, p):
        """
            expressao_aditiva : expressao_multiplicativa
                | expressao_aditiva operador_soma expressao_multiplicativa
        """
        if(len(p) == 2):
            p[0] = Tree('expressao_aditiva', [p[1]])
        elif(len(p) == 4):
            p[0] = Tree('expressao_aditiva', [p[1], p[2], p[3]])

    def p_expressao_multiplicativa(self, p):
        """
            expressao_multiplicativa : expressao_unaria
                | expressao_multiplicativa operador_multiplicacao expressao_unaria
        """
        if(len(p) == 2):
            p[0] = Tree('expressao_multiplicativa', [p[1]])
        elif(len(p) == 4):
            p[0] = Tree('expressao_multiplicativa', [p[1], p[2], p[3]])

    def p_expressao_unaria(self, p):
        """
            expressao_unaria : fator
                | operador_soma fator
                | operador_negacao fator
        """
        if(len(p) == 2):
            p[0] = Tree('expressao_unaria', [p[1]])
        else:
            p[0] = Tree('expressao_unaria', [p[1], p[2]])

    def p_operador_relacional(self, p):
        """
            operador_relacional : MENOR
                | MAIOR
                | IGUAL
                | DIFERENTE
                | MENOR_IGUAL
                | MAIOR_IGUAL
        """
        p[0] = Tree('operador_relacional', [], str(p[1]), p.lineno(1))

    def p_operador_soma(self, p):
        """
            operador_soma : MAIS
                | MENOS
        """
        p[0] = Tree('operador_soma', [], str(p[1]), p.lineno(1))

    def p_operador_logico(self, p):
        """
            operador_logico : E_LOGICO
                | OU_LOGICO
        """
        p[0] = Tree('operador_logico', [], str(p[1]))

    def p_operador_negacao(self, p):
        """
            operador_negacao : NEGACAO
        """
        p[0] = Tree('operador_negacao', [], str(p[1]), p.lineno(1))

    def p_operador_multiplicacao(self, p):
        """
            operador_multiplicacao : MULTIPLICACAO
                | DIVISAO
        """
        p[0] = Tree('operador_multiplicacao', [], str(p[1]))

    def p_fator(self, p):
        """
            fator : ABRE_COLCHETE expressao FECHA_COLCHETE
                | var
                | chamada_funcao
                | numero
        """
        if(len(p) == 4):
            p[0] = Tree('fator', [p[2]])
        else:
            p[0] = Tree('fator', [p[1]])

    def p_numero_inteiro(self, p):
        """
            numero : INTEIRO
        """
        p[0] = Tree('inteiro', [], str(p[1]), p.lineno(1))

    def p_numero_flutuante(self, p):
        """
            numero : FLUTUANTE
        """
        p[0] = Tree('flutuante', [], str(p[1]), p.lineno(1))

    def p_numero_notacao_cientifica(self, p):
        """
            numero : NOTACAO_CIENTIFICA
        """
        p[0] = Tree('cientifica', [], str(p[1]), p.lineno(1))

    def p_chamada_funcao(self, p):
        """
            chamada_funcao : ID ABRE_PARENTESE lista_argumentos FECHA_PARENTESE
        """
        p[0] = Tree('chamada_funcao', [p[3]], p[1])

    def p_lista_argumentos(self, p):
        """
            lista_argumentos : lista_argumentos VIRGULA expressao
                | expressao
        """
        if(len(p) == 4):
            p[0] = Tree('lista_argumentos', [p[1], p[3]])
        else:
            p[0] = Tree('lista_argumentos', [p[1]])

    def p_vazio(self, p):
        """vazio : """

# erros

    def p_indice_error(self, p):
        """
            indice : ABRE_COLCHETE  error
                | error  FECHA_COLCHETE
                | ABRE_COLCHETE error FECHA_COLCHETE
                | indice ABRE_COLCHETE  error
                | indice error  FECHA_COLCHETE
                | indice ABRE_COLCHETE error FECHA_COLCHETE
        """
        print("Análise sintática -> Erro de indexação \n")

    def p_cabecalho_error(self, p):
        """
            cabecalho : ID ABRE_PARENTESE error FECHA_PARENTESE error FIM
        """
        print("Análise sintática -> Erro no cabeçalho \n")

    def p_se_error(self, p):
        """
            se : SE error ENTAO error FIM
                | SE error ENTAO error SENAO error FIM
        """
        print("Análise sintática -> Erro na expressão SE \n")

    def p_repita_error(self, p):
        """
            repita : REPITA error ATE error
        """
        print("Análise sintática -> Erro na expressão REPITA \n")

    def p_leia_error(self, p):
        """
            leia : LEIA ABRE_PARENTESE error FECHA_PARENTESE
        """
        print("Análise sintática -> Erro na expressão LEIA \n")

    def p_error(self , p):
        if(p):
            print("Análise sintática -> Erro no '%s', na linha: %d" % (p.value, p.lineno))
        else:
            print('Análise sintática -> Erro')
