import ply.lex as lex

class Lexica:
  reservadas = {
    'repita': 'REPITA',
    'até': 'ATE',
    'então': 'ENTAO',
    'escreva': 'ESCREVA',
    'fim': 'FIM',
    'flutuante': 'FLUTUANTE',
    'inteiro': 'INTEIRO',
    'leia': 'LEIA',
    'retorna': 'RETORNA',
    'se': 'SE',
    'senão': 'SENAO'
  }
      
  tokens = [  
    'ABRE_CHAVES',
    'ABRE_COLCHETE',
    'ABRE_PARENTESE',
    'ATE',
    'ATRIBUICAO',
    'DIFERENTE',
    'DIVISAO',
    'DOIS_PONTOS',
    'ENTAO',
    'ESCREVA',
    'E_LOGICO',
    'FECHA_CHAVES',
    'FECHA_COLCHETE', 
    'FECHA_PARENTESE',
    'FIM',
    'FLUTUANTE',
    'ID',
    'IGUAL', 
    'INTEIRO',
    'LEIA',
    'MAIOR', 
    'MAIS',
    'MAIOR_IGUAL',
    'MENOR',
    'MENOS',
    'MENOR_IGUAL',
    'MULTIPLICACAO',
    'NEGACAO',
    'OU_LOGICO',
    'REPITA',
    'RETORNA',
    'SE',
    'SENAO',
    'VIRGULA'
  ]  
  
  t_ABRE_CHAVES = r'\{'
  t_ABRE_COLCHETE = r'\['
  t_ABRE_PARENTESE = r'\('
  T_ATRIBUICAO = r'\:\='
  t_DIFERENTE = r'\<>'
  t_DIVISAO = r'/'
  t_DOIS_PONTOS = r'\:'
  t_E_LOGICO = r'\&\&'
  t_FECHA_CHAVES = r'\}'
  t_FECHA_COLCHETE = r'\]'
  t_FECHA_PARENTESE = r'\)'
  t_ignore = ' \t'
  t_IGUAL = r'\='
  t_MAIOR = r'\>'
  t_MAIS = r'\+'
  t_MAIOR_IGUAL = r'\>\='
  t_MENOR = r'\<'
  t_MENOS = r'\-'
  t_MENOR_IGUAL = r'\<\='
  t_MULTIPLICACAO = r'\*'
  t_NEGACAO = r'\!'
  t_OU_LOGICO = r'\|\|'
  t_VIRGULA = r'\,'

  def __init__(self):
    self.lexer = lex.lex(debug=False, module=self, optimize=False)

  def t_COMENTARIO(self, t):
    r'\{[^}]*[^{]*\}'
    numeroLinhas = t.value.count("\n")
    t.lexer.lineno += numeroLinhas
    pass

  def t_error(self, t):
    print("ERRO - O Caractere '", t.value[0], "' nao e reconhecido")
    t.lexer.skip(1)

  def t_FLUTUANTE(self, t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

  def t_ID(self, t):
    r'[a-zA-Z_à-ú][a-zA-Z_0-9à-ú]*'
    t.type = self.reservadas.get(t.value, 'ID')
    return t

  def t_INTEIRO(self, t):
    r'\d+'
    t.value = int(t.value)
    return t

  def t_NOVA_LINHA(self, t):
    r'\n+'
    t.lexer.lineno += len(t.value)

  def t_NOTACAO_CIENTIFICA(self, t):
    r'\d+\.?\d*e[+|-]?\d+'
    t.type = self.reservadas.get(t.value, 'NOTACAO_CIENTIFICA')
    return t

  def readFile(self, file):
    try:
      arq = open(file, encoding='utf8')
      lex.input(arq.read())
    except:
      print('ERRO - Nao Foi Possivel Abrir o Arquivo, Por Favor Tente Novamente')

  def printTokens(self):
    linhaAtual = 0
    linhaToken = 0
    while True:
      tok = lex.token()
      if not tok:
        break
      linhaToken = tok.lineno
      if(linhaAtual < linhaToken):
        linhaAtual = linhaToken
        print("-------------- Linha ", linhaAtual, " --------------")
      print("Token: ", tok.type, " --- Valor: ", tok.value)