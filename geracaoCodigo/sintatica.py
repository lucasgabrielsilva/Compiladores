
import ply.yacc as yacc
import sys
import ply.lex as lex
from tree import Tree

class Sintatica:
    def __init__(self, data, tokens):
        
        self.tokens = tokens
        self.precedence = (
            ('left', 'IGUAL', 'MAIOR_IGUAL', 'MAIOR', 'MENOR_IGUAL', 'MENOR'),
            ('left', 'MAIS', 'MENOS'),
            ('left', 'MULTIPLICACAO', 'DIVISAO'),
        )

        a = yacc.yacc(debug=False, module=self, optimize=False)
        self.ast = a.parse(data)

    
    
    def p_programa(self, p):
        '''programa : lista_declaracoes'''

        p[0] = Tree('programa', [p[1]])

    def p_lista_declaracoes(self, p):
        '''lista_declaracoes : lista_declaracoes declaracao
        | declaracao'''

        if len(p) == 3:
            p[0] = Tree('lista_declaracoes', [p[1], p[2]])
        else:
            p[0] = Tree('lista_declaracoes', [p[1]])

    def p_declaracao(self, p):
        '''declaracao : declaracao_variaveis
        | inicializacao_variaveis
        | declaracao_funcao'''

        p[0] = Tree('declaracao', [p[1]], '', p.lineno(1))

    def p_declaracao_variaveis(self, p):
        '''declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis'''

        p[0] = Tree('declaracao_variaveis', [p[1], p[3]])


    def p_inicializacao_variaveis(self, p):
        '''inicializacao_variaveis : atribuicao'''

        p[0] = Tree('inicializacao_variaveis', [p[1]])

    def p_lista_variaveis(self, p):
        '''lista_variaveis : lista_variaveis VIRGULA var
        | var'''

        if len(p) == 4:
            p[0] = Tree('lista_variaveis', [p[1], p[3]])
        else:
            p[0] = Tree('lista_variaveis', [p[1]])

    def p_var(self, p):
        '''var : ID
        | ID indice'''

        # node_aux = p[0]

        if len(p) == 2:
            # h = Tree('ID', [p[1]], p[1], p.lineno(1))
            p[0] = Tree('var', [], p[1], p.lineno(1))
            # print(p[0].value)
        else:
            p[0] = Tree('var', [p[2]], p[1], p.lineno(1))

    def p_indice(self, p):
        '''indice : indice ABRE_COLCHETE expressao FECHA_COLCHETE
        | ABRE_COLCHETE expressao FECHA_COLCHETE'''

        if len(p) == 5:
            p[0] = Tree('indice', [p[1], p[3]])
        else:
            p[0] = Tree('indice', [p[2]])

    def p_tipo(self, p):
        '''tipo : INTEIRO
        | FLUTUANTE'''

        p[0] = Tree('tipo', [], p[1])

    def p_declaracao_funcao(self, p):
        '''declaracao_funcao : tipo cabecalho
        | cabecalho'''

        if len(p) == 3:
            p[0] = Tree('declaracao_funcao', [p[1], p[2]], '', p.lineno(2))
        else:
            p[0] = Tree('declaracao_funcao', [p[1]], '', p.lineno(1))

    def p_cabecalho(self, p):
        '''cabecalho : ID ABRE_PARENTESE lista_parametros FECHA_PARENTESE corpo FIM'''

        p[0] = Tree('cabecalho', [p[3], p[5], Tree(type_node=p[6])], p[1])

    def p_lista_parametros(self, p):
        '''lista_parametros : lista_parametros VIRGULA parametro
        | parametro
        | vazio '''

        if len(p) == 4:
            p[0] = Tree('lista_parametros', [p[1], p[3]])
        else: 
            p[0] = Tree('lista_parametros', [p[1]])

    def p_parametro(self, p):
        '''parametro : tipo DOIS_PONTOS ID
        |  parametro ABRE_COLCHETE FECHA_COLCHETE'''

        if p[2] == ':':
            p[0] = Tree('parametro', [p[1]], p[3])
        else:
            p[0] = Tree('parametro', [p[1]])

    def p_corpo(self, p):
        '''corpo : corpo acao
        | vazio'''

        if len(p) == 3:
            p[0] = Tree('corpo', [p[1], p[2]])
        else:
            p[0] = Tree('corpo', [p[1]])

    def p_acao(self, p):
        '''acao : expressao
        | declaracao_variaveis
        | se
        | repita
        | leia
        | escreva
        | retorna'''

        p[0] = Tree('acao', [p[1]])

    def p_se(self, p):
        '''se : SE expressao ENTAO corpo FIM
        | SE expressao ENTAO corpo SENAO corpo FIM'''

        if len(p) == 6:
            p[0] = Tree('se', [p[2], p[4], Tree(type_node=p[5])])
        else:
            p[0] = Tree('se', [p[2], p[4], p[6], Tree(type_node=p[7])])

    def p_repita(self, p):
        '''repita : REPITA corpo ATE expressao'''

        p[0] = Tree('repita', [p[2], p[4], Tree(type_node=p[3])])

    def p_leia(self, p):
        '''leia : LEIA ABRE_PARENTESE var FECHA_PARENTESE'''

        p[0] = Tree('leia', [p[3]],'' ,p.lineno(1))
    
    def p_escreva(self, p):
        '''escreva : ESCREVA ABRE_PARENTESE expressao FECHA_PARENTESE '''

        p[0] = Tree('escreva', [p[3]],'' ,p.lineno(1))
    
    def p_retorna(self, p):
        '''retorna : RETORNA ABRE_PARENTESE expressao FECHA_PARENTESE '''

        p[0] = Tree('retorna', [p[3]],'' ,p.lineno(1))
    
    def p_atribuicao(self, p):
        '''atribuicao : var ATRIBUICAO expressao'''

        p[0] = Tree('atribuicao', [p[1], p[3]], '', p.lineno(2))

    def p_expressao(self, p):
        '''expressao : expressao_logica
        | atribuicao'''

        p[0] = Tree('expressao', [p[1]])

    def p_operador_relacional(self, p):
        '''operador_relacional : MENOR
        | MAIOR
        | IGUAL
        | DIFERENTE
        | MENOR_IGUAL
        | MAIOR_IGUAL'''

        p[0] = Tree('operador_relacional', [], str(p[1]), p.lineno(1))

    def p_operador_soma(self, p):
        '''operador_soma : MAIS
        | MENOS'''

        p[0] = Tree('operador_soma', [], str(p[1]), p.lineno(1))
    
    def p_operador_logico(self, p):
        '''operador_logico : E_LOGICO
        | OU_LOGICO
        | NEGACAO'''

        p[0] = Tree('operador_logico', [], str(p[1]))

    def p_operador_multiplicacao(self, p):
        '''operador_multiplicacao : MULTIPLICACAO
        | DIVISAO'''

        p[0] = Tree('operador_multiplicacao', [], str(p[1]))
        
    def p_fator(self, p):
        '''fator : ABRE_PARENTESE expressao FECHA_PARENTESE
        | var
        | chamada_funcao
        | numero_int
        | numero_float'''

        if len(p) == 2:
            p[0] = Tree('fator', [p[1]])
        else:
            p[0] = Tree('fator', [p[2]])
        
    def p_numero_int(self, p):
        '''numero_int : INTEIRO'''

        p[0] = Tree('numero_int', [], p[1])
    
    def p_numero_float(self, p):
        '''numero_float : FLUTUANTE'''

        p[0] = Tree('numero_float', [], float(p[1]), p.lineno(1))
    
    def p_chamada_funcao(self, p):
        '''chamada_funcao : ID ABRE_PARENTESE lista_argumentos FECHA_PARENTESE'''

        p[0] = Tree('chamada_funcao', [p[3]], p[1])
    
    def p_lista_argumentos(self, p):
        '''lista_argumentos : lista_argumentos VIRGULA expressao
        | expressao
        | vazio'''

        if len(p) == 2:
            p[0] = Tree('lista_argumentos', [p[1]])
        else:
            p[0] = Tree('lista_argumentos', [p[1], p[3]])

    def p_expressao_logica(self, p):
        '''expressao_logica : expressao_simples
        | expressao_logica operador_logico expressao_simples'''

        if len(p) == 2:
            p[0] = Tree('expressao_logica', [p[1]])
        else:
            p[0] = Tree('expressao_logica', [p[1], p[2], p[3]])

    def p_expressao_simples(self,p):
        '''expressao_simples : expressao_aditiva
        | expressao_simples operador_relacional expressao_aditiva'''

        if len(p) == 2:
            p[0] = Tree('expressao_simples', [p[1]])
        else:
            p[0] = Tree('expressao_simples', [p[1], p[2], p[3]])

    def p_expressao_aditiva(self, p):
        '''expressao_aditiva : expressao_multiplicativa
        | expressao_aditiva operador_soma expressao_multiplicativa'''

        if len(p) == 2:
            p[0] = Tree('expressao_aditiva', [p[1]])
        else:
            p[0] = Tree('expressao_aditiva', [p[1], p[2], p[3]])

    def p_expressao_multiplicativa(self, p):
        '''expressao_multiplicativa : expressao_unaria
        | expressao_multiplicativa operador_multiplicacao expressao_unaria'''

        if len(p) == 2:
            p[0] = Tree('expressao_multiplicativa', [p[1]])
        else:
            p[0] = Tree('expressao_multiplicativa', [p[1], p[2], p[3]])                    

    def p_expressao_unaria(self, p):
        '''expressao_unaria : fator
        | operador_soma fator'''

        if len(p) == 2:
            p[0] = Tree('expressao_unaria', [p[1]])
        else:
            p[0] = Tree('expressao_unaria', [p[1], p[2]])

    def p_vazio(self, p):
        '''vazio : '''

        p[0] = Tree('vazio')
        pass

    
    ####### Declaração de erros #######
    
    def p_error(self, p):
        if p:
            print("Analise sintatica -> Erro '%s' na linha '%d'" %(p.value, p.lineno))
        else:
            print("Analise sintatica -> Erro!")
    
    def p_leia_error(self, p):
        '''leia : LEIA ABRE_PARENTESE error FECHA_PARENTESE'''

        print("Analise sintatica -> Erro de leitura (Argumento Inválido)")

    def p_escreva_error(self, p):
        '''escreva : ESCREVA ABRE_PARENTESE error FECHA_PARENTESE '''

        print("Analise sintatica -> Erro de escrita (Argumento Inválido)")

    def p_retorna_error(self, p):
        '''retorna : RETORNA ABRE_PARENTESE error FECHA_PARENTESE'''

        print("Analise sintatica -> Erro de retorno (Argumento Inválido)")

    def p_declaracao_variaveis_error(self, p):
        '''declaracao_variaveis : error DOIS_PONTOS lista_variaveis'''

        print("Analise sintatica -> Erro de declaração de variáveis")
        
    def p_atribuicao_error(self, p):
        '''atribuicao : var ATRIBUICAO error
        | error ATRIBUICAO expressao'''

        print("Analise sintatica -> Erro de atribuição")
    
    def p_lista_declaracoes_error(self, p):
        '''lista_declaracoes : error error
        | error'''
        print("Analise sintatica -> Erro na lista de declaração")

    def p_indice_error(self, p):
        '''indice : indice ABRE_COLCHETE error FECHA_COLCHETE
        | ABRE_COLCHETE error FECHA_COLCHETE'''
        print("Analise sintatica -> Erro de índice")
    
    def p_acao_error(self, p):
        '''acao : error'''
        print("Analise sintatica -> Erro de ação")

    def p_cabecalho_error(self, p):
        '''cabecalho : ID ABRE_PARENTESE lista_parametros FECHA_PARENTESE error FIM'''

        print("Analise sintatica -> Erro no cabeçalho da função")

    def p_repita_error(self, p):
        '''repita : REPITA error ATE error'''
        print("Analise sintatica -> Erro no laço 'REPITA'")

    def p_declaracao_error(self, p):
        '''declaracao : error'''
        print("Analise sintatica -> Erro de declaração")
    
    def p_inicializacao_variaveis_error(self, p):
        '''inicializacao_variaveis : error'''
        print("Analise sintatica -> Erro na inicialização de variável")
    
    def p_lista_variaveis_error(self, p):
        '''lista_variaveis : error VIRGULA error
        | error'''
        print("Analise sintatica -> Erro em lista de variáveis")

    def p_declaracao_funcao_error(self, p):
        '''declaracao_funcao : error error
        | error'''
        print("Analise sintatica -> Erro na declaração de função")
    
    def p_lista_parametros_error(self, p):
        '''lista_parametros : error VIRGULA error
        | error '''
        print("Analise sintatica -> Erro na lista de parametros")
    
    def p_corpo_error(self, p):
        '''corpo : error error
        | error'''
        print("Analise sintatica -> Erro no corpo da função")
    
    def p_se_error(self, p):
        '''se : SE error ENTAO error FIM
        | SE error ENTAO error SENAO error FIM'''
        print("Analise sintatica -> Erro na condição 'SE'")

    def p_expressao_error(self, p):
        '''expressao : error'''
        print("Analise sintatica -> Erro de expressão")

    def p_expressao_simples_error(self,p):
        '''expressao_simples : error
        | error error error'''
        print("Analise sintatica -> Erro na expressão")
