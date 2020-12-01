from node import Node
from functionData import FunctionData

class TabSymbols():

	def __init__(self, ast):
		
		self.symbols = []
		self.funcoes = []
		self.makeTabSymbols("global", ast)
		self.typeNode("global", ast)

	def percoreTree(self, node):
		while(node != None and len(node.child) == 1 and node.type != "var" and node.type != "chamada_funcao"):
			node = node.child[0]
		return node		
	
	def typeNode(self, scope, node): 
		if node != None:
			if node.type == "cabecalho": 
				scope = node.value
			elif node.type == "se": 
				self.condicional(node, scope) 
			elif node.type == "atribuicao": 
				self.atribuicao(node, scope) 
			elif node.type == "retorna": 
				self.retorna(scope, node) 
			elif node.type == "chamada_funcao":
				self.chamada_funcao(node, scope)
			elif node.type == "var":
				if len(node.child) > 0:
					self.verificarIndiceVetor(node, scope)
			elif node.type == "declaracao_funcao":
				self.declaracaoFuncao(node)
			for filho in node.child:
				self.typeNode(scope, filho)
	
	def makeTabSymbols(self, scope, node): 
		if node != None:
			if node.type == "cabecalho":
				scope = node.value
			elif node.type == "declaracao_variaveis":
				self.addTabSymbols(scope, node) 
			elif node.type == "parametro":
				self.parametro(scope, node)
			for filho in node.child:
				self.makeTabSymbols(scope, filho)

	def parametro(self, scope, node):
		if len(node.child) > 0:
			node = Node(scope, node.child[0], node.value, "var")
			self.symbols.append(node)

	def addTabSymbols(self, scope, node): 				
		type = node.child[0].type 								
		lv = node.child[1]
		self.listaVariaveis(lv, scope, type) 								
		
	def listaVariaveis(self, node, scope, type):
		corpo = "var"
		if(len(node.child[0].child)> 0):
			if node.child[0].child[0].type == "indice":
				corpo = "array"
			node = Node(scope, type, node.child[0].value, corpo)
			self.symbols.append(node)	
		else:
			node = Node(scope, type, node.child[0].value, corpo)
			self.symbols.append(node)	
			return

	def condicional(self, node, scope): 
		node = node.child[0]
		var1 = None
		var2 = None
		if len(node.child) == 1:
			node = node.child[0]
			var1 = self.percoreTree(node.child[0])
			var2 = self.percoreTree(node.child[2])
		if var1.type == 'var':
			type1 = self.verificaDeclaracao(var1.value, scope)
		else:
			type1 = self.typeVar(var1.value)
		if var2.type == 'var':
			type2 = self.verificaDeclaracao(var2.value, scope)
		else:
			type2 = self.typeVar(var2.value)

	def declaracaoFuncao(self, node):
		args = []
		if len(node.child) > 1:
			nome = node.child[1].value
			type = node.child[0].type
			args = self.cabecalho(node.child[1], args)
		else:
			nome = node.child[0].value
			type = "vazio"
			args = self.cabecalho(node.child[0], args)
		funcao = FunctionData(type, nome, args)
		self.funcoes.append(funcao)	

	def cabecalho(self, node, args):
		if node == None:
			return []
		if node.child[0] != None:
			args = self.lista_parametros(node.child[0], args)
			return args

	def atribuicao(self, node, scope):
		types = []
		leftVar = node.child[0]
		lefttype = self.verificaDeclaracao(leftVar.value, scope)
		types.append(lefttype)
		right = self.percoreTree(node.child[1])
		if right.type == 'var':
			type = self.verificaDeclaracao(right.value, scope)			
			if type == None:
				print ("Erro: Variavel " +  right.child[0].value + " é está sendo usada, mas não foi declarada")
			else: types.append(type)
		elif right.type == 'inteiro' or right.type == 'flutuante' or right.type == 'cientifica':
			type = self.typeVar(right.value)
			types.append(type)
		if right.type == 'expressao_simples':
			type_expr = self.expressao_simples(right, scope)
			types.append(type_expr)
		elif right.type == 'expressao_aditiva':
			type_expr = self.expressao_aditiva(right, scope)
			types.append(type_expr)
		elif right.type == 'expressao_multiplicativa':
			type_expr = self.expressao_multiplicativa(right, scope)
			types.append(type_expr)
		elif right.type == 'expressao_unaria':
			type_expr = self.expressao_unaria(right, scope)
			types.append(type_expr)
		for i in range(0, len(types)):
			if types[0] != types[i]:
				aux = types[i]
				if(aux != False):
					aux2 = types[0]
					print("Aviso: Coerção implícita do valor atribuído para " + node.child[0].value + ", variável "+ node.child[0].value + " " + str(aux2) + " recebendo um " + aux)
					break

	def expressao_simples(self, node, scope):	
		if len(node.child) == 1:
			folha = self.percoreTree(node)
			if folha.type == 'var':
				return self.verificaDeclaracao(folha.value, scope)
			elif folha.type == 'inteiro' or folha.type == 'flutuante' or folha.type == 'cientifico':
				return self.typeVar(folha.value)
			elif folha.type == 'expressao_aditiva':
				return self.expressao_aditiva(folha, scope)
			elif folha.type == 'expressao_multiplicativa':
				return self.expressao_multiplicativa(folha, scope)
			elif folha.type == 'expressao_unaria':
				return self.expressao_unaria(folha, scope)
		else:
			type1 = self.expressao_simples(node.child[0], scope)
			type2 = self.expressao_aditiva(node.child[2], scope)
			if type1 != type2:
				return False 
			else:
				return type1 

	def expressao_aditiva(self, node, scope):
		if len(node.child) == 1:
			folha = self.percoreTree(node)
			if folha.type == 'var':
				return self.verificaDeclaracao(folha.value, scope)
			elif folha.type == 'inteiro' or folha.type == 'flutuante' or folha.type == 'cientifica':
				return self.typeVar(folha.value)
			elif folha.type == 'expressao_multiplicativa':
				return self.expressao_multiplicativa(folha, scope)
			elif folha.type == 'expressao_unaria':
				return self.expressao_unaria(folha, scope)
		else:
			type1 = self.expressao_aditiva(node.child[0], scope)
			type2 = self.expressao_unaria(node.child[2], scope)
			if type1 != type2:
				return False
			else:
				return type1

	def expressao_multiplicativa(self, node, scope):
		if len(node.child) == 1:
			folha = self.percoreTree(node)
			if folha.type == 'var':
				return self.verificaDeclaracao(folha.value, scope)
			elif folha.type == 'inteiro' or folha.type == 'flutuante' or folha.type == 'cientifica':
				return self.typeVar(folha.value)
			elif folha.type == 'expressao_unaria':
				return self.expressao_unaria(folha, scope)
		else:
			type1 = self.expressao_aditiva(node.child[0], scope)
			type2 = self.expressao_multiplicativa(node.child[2], scope)
			if type1 != type2:
				return False
			else:
				return type1
	
	def expressao_unaria(self, node, scope):
		if len(node.child) == 1:
			folha = self.percoreTree(node)
			if folha.type == 'var':
					return self.verificaDeclaracao(folha.value, scope)
			elif folha.type == 'inteiro' or folha.type == 'flutuante' or folha.type == 'cientifica':
					return self.typeVar(folha.value)
		else:
			type1 = self.percoreTree(node.child[0])
			if type1.type == 'var':
				return self.verificaDeclaracao(type1.value, scope)
			elif type1.type == 'inteiro' or type1.type == 'flutuante' or type1.type == 'cientifica':
				return self.typeVar(type1.value)
	
	def verificaDeclaracao(self, var, scope):
		for x in self.symbols:
			if str(x.value) == str(var) and str(x.scope) == str(scope):
				x.used = 1
				return str(x.type)
		for x in self.symbols:
			if str(x.value) == str(var) and str(x.scope) == "global":
				x.used = 1
				return str(x.type)
		
		print ("Erro: Variável " + var + " não declarada.")
		return False
	
	def retorna(self, scope, node):
		y = self.percoreTree(node)
		type = ''
		if y.type == "var":
			type = self.verificaDeclaracao(y.value, scope)
		elif y.type == "inteiro" or y.type == "flutuante" or y.type == "cientifica":
			type = self.typeVar(y.value)
		elif y.type == "expressao_simples":
			type = self.expressao_simples(y, scope)
		elif y.type == "expressao_aditiva":
			type = self.expressao_aditiva(y, scope)
		elif y.type == "expressao_multiplicativa":
			type = self.expressao_multiplicativa(y, scope)
		elif y.type == "expressao_unaria":
			type = self.expressao_unaria(y, scope)
		for funcao in self.funcoes:
			if funcao.type != type and funcao.name == scope: 
				print ("Erro: A função " + scope + " deve retornar " + funcao.type + ".")
				break
			if funcao.type == type and funcao.name == scope:
				funcao.retorno = 1
				break

	def chamada_funcao(self, node, scope):
		if node.value == "principal" and scope == "principal":
			print ("Aviso: Chamada recursiva para a função principal")
		for i in self.funcoes: 
			l = 0
			if i.name == node.value:
				i.used = 1 	
				l = l + 1
				if node.child[0] == None:
					return False
				args = self.lista_argumentos(node.child[0], scope, [])
				if args != None:
					if len(args) != len(i.parameters) :
						print ("Erro: Chamada a função " + i.name + " com número de parâmetros menor que o declarado")
						return False
					else:
						for j in range(0,len(args)):
							if args[j] != i.parameters[j]:
								print ("Erro: tipos incompatíveis no argumento. Argumento " + str(j+1) + " deve ser um " + str(i.parameters[j]) + ". Função " + str(i.name) + ".")
								return False
						return True
			else:
				print("Aviso: Função " + i.name + " declarada, mas não usada.")
		print("Aviso: Função " + node.value + " é utilizada mas não foi declarada.")

	def args_chamadaFunc(self, node, args, scope):
		if node == None:
			return args
		if len(node.child) == 1:
			if node.child[0] != None:
				folha = self.percoreTree(node.child[0])
				if folha.type == "var":
					type = self.verificaDeclaracao(folha.value, scope)
					if type != None:
						return type		
				elif folha.type == "inteiro" or folha.type == "flutuante" or folha.type == "cientifica":
					type = self.typeVar(folha.value)
					return type		
		else:
			for filho in node.child:
				type = self.args_chamadaFunc(filho, args, scope)
				if type == 'inteiro' or type == 'flutuante':
					args.append(type)
			return args
			
	def lista_parametros(self, node, args):
		for no in node.child:
			if node.type == "lista_parametros":
				args = self.lista_parametros(no, args)
			y = self.percoreTree(no)			
			if y.type != "lista_parametros":
				args.append(y.type)
				return args
			else:
				args = self.lista_parametros(y, args)

	def lista_argumentos(self, node, scope, args):
		for no in node.child:
			if args == None:
				print ("Erro: Lista de argumentos inválida.")
			y = self.percoreTree(no)
			if y.type == "expressao_simples":
				type = self.expressao_simples(y, scope)
				if type == "flutuante" or type == "inteiro":
					args.append(type)
					return args 
			elif y.type == "expressao_multiplicativa":
				type = self.expressao_multiplicativa(y, scope)
				if type == "flutuante" or type == "inteiro":
					args.append(type)
					return args 
			elif y.type == "expressao_aditiva":
				type = self.expressao_aditiva(y, scope)
				if type == "flutuante" or type == "inteiro":
					args.append(type)
					return args 
			elif y.type == "expressao_unaria":
				type = self.expressao_unaria(y, scope)
				if type == "flutuante" or type == "inteiro":
					args.append(type)
					return args 
			elif y.type == "var":
				type = self.verificaDeclaracao(y.value, scope)
				args.append(type)
			elif y.type == "inteiro" or y.type == "flutuante" or y.type == "cientifica":
				type = self.typeVar(y.value)
				args.append(type)
				return args 
			else:
				args = self.lista_argumentos(y,scope ,args)
			return args

	def typeVar(self, num):
		try:
			num = int(num)
		except Exception:
			num = float(num)
		if type(num) == float:
			return "flutuante"
		elif type(num) == int:
			return "inteiro"
	
	def verificarIndiceVetor(self, node, scope):
		actual = self.percoreTree(node.child[0])
		tipo = ""
		if actual.type == "var":
			tipo = self.verificaDeclaracao(actual.value, scope)
		elif actual.type == "inteiro" or actual.type == "flutuante" or actual.type == "cientifica":
			tipo = self.typeVar(actual.value)
		elif actual.type == "expressao_simples":
			tipo = self.expressao_simples(actual, scope)
		elif actual.type == "expressao_aditiva":
			tipo = self.expressao_aditiva(actual, scope)
		elif actual.type == "expressao_multiplicativa":
			tipo = self.expressao_multiplicativa(actual, scope)
		elif actual.type == "expressao_unaria":
			tipo = self.expressao_unaria(actual, scope)
		if actual.type == "flutuante":
			print ("Erro: Indice do vetor "+ node.value +" deve ser inteiro.")

	def printTab(self):
		for symbols in self.symbols:
			print("Lexema : {}, type: {}, escopo: {}".format(symbols.value, symbols.type, symbols.scope))
